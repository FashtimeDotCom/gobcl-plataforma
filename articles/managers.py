# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter

import datetime
from operator import attrgetter

from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import activate

from aldryn_apphooks_config.managers.base import ManagerMixin, QuerySetMixin
from parler.managers import TranslatableManager, TranslatableQuerySet
from taggit.models import Tag, TaggedItem

from searches.elasticsearch.documents import SearchIndex
from elasticsearch_dsl import connections
from elasticsearch.helpers import bulk


class ArticleQuerySet(QuerySetMixin, TranslatableQuerySet):
    def exclude_article(self, article):
        return self.exclude(Q(id=article.id) | Q(id=article.public_id))

    def draft(self):
        """
        Returns articles that are drafts
        """
        return self.filter(is_draft=True)

    def not_draft(self):
        """
        Returns articles that are not drafts
        """
        return self.filter(is_draft=False)

    def published(self):
        """
        Returns articles that are published AND have a publishing_date that
        has actually passed.
        """
        return self.filter(
            publishing_date__lte=now(),
            is_draft=False,
        ).translated(is_published=True)

    def filter_tag(self, tag):
        """
        Returns all the articles with the specified tag.
        """
        return self.filter(tags=tag)

    def exclude_tag(self, tag):
        """
        Returns all the articles without the specified tag.
        """
        return self.exclude(tags=tag)


class RelatedManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        qs = ArticleQuerySet(self.model, using=self.db)
        return qs.select_related('featured_image')

    def exclude_article(self, article):
        return self.get_queryset().exclude_article(article)

    def draft(self):
        return self.get_queryset().draft()

    def published(self):
        return self.get_queryset().published()

    def filter_tag(self, tag):
        return self.get_queryset().filter_tag(tag)

    def exclude_tag(self, tag):
        return self.get_queryset().exclude_tag(tag)

    def get_months(self, request, namespace):
        """
        Get months and years with articles count for given request and
        namespace string. This means how many articles there are in each month.

        The request is required, because logged-in content managers may get
        different counts.

        Return list of dictionaries ordered by article publishing date of the
        following format:
        [
            {
                'date': date(YEAR, MONTH, ARBITRARY_DAY),
                'num_articles': NUM_ARTICLES
            },
            ...
        ]
        """

        # TODO: check if this limitation still exists in Django 1.6+
        # This is done in a naive way as Django is having tough time while
        # aggregating on date fields
        if (request and hasattr(request, 'toolbar') and
                request.toolbar and request.toolbar.edit_mode):
            articles = self.namespace(namespace)
        else:
            articles = self.published().namespace(namespace)
        dates = articles.values_list('publishing_date', flat=True)
        dates = [(x.year, x.month) for x in dates]
        date_counter = Counter(dates)
        dates = set(dates)
        dates = sorted(dates, reverse=True)
        months = [
            # Use day=3 to make sure timezone won't affect this hacks'
            # month value. There are UTC+14 and UTC-12 timezones!
            {'date': datetime.date(year=year, month=month, day=3),
             'num_articles': date_counter[(year, month)]}
            for year, month in dates]
        return months

    def get_tags(self, request, namespace):
        """
        Get tags with articles count for given namespace string.

        Return list of Tag objects ordered by custom 'num_articles' attribute.
        """
        if (request and hasattr(request, 'toolbar') and
                request.toolbar and request.toolbar.edit_mode):
            articles = self.namespace(namespace)
        else:
            articles = self.published().namespace(namespace)
        if not articles:
            # return empty iterable early not to perform useless requests
            return []
        kwargs = TaggedItem.bulk_lookup_kwargs(articles)

        # aggregate and sort
        counted_tags = dict(TaggedItem.objects
                            .filter(**kwargs)
                            .values('tag')
                            .annotate(tag_count=models.Count('tag'))
                            .values_list('tag', 'tag_count'))

        # and finally get the results
        tags = Tag.objects.filter(pk__in=counted_tags.keys())
        for tag in tags:
            tag.num_articles = counted_tags[tag.pk]
        return sorted(tags, key=attrgetter('num_articles'), reverse=True)

    def bulk_index(self, boost=1, all=True, archived=False):
        languages = ('es', 'en')
        print()
        print('=' * 30)
        if all:
            print('Articles')
        else:
            if archived:
                print('Archived articles')
            else:
                print('Current articles')
        for language in languages:
            print('Language:', language)
            activate(language)
            articles = self.get_queryset().translated(
                title__isnull=False,
                is_published=True,
            ).filter(
                publishing_date__lte=now(),
                is_draft=False,
            )

            # Bulk indexing using the elasticsearch library instead of
            # elasticsearch_dsl, to use the method bulk and index documents
            # more efficiently
            documents = []
            value = 1
            if not all:
                tag = None
                if language == 'es':
                    tag = Tag.objects.get_or_create(name='archivo')[0]
                elif language == 'en':
                    tag = Tag.objects.get_or_create(name='archive')[0]

                if archived:
                    articles = articles.filter_tag(tag)
                else:
                    articles = articles.exclude_tag(tag)

            total = articles.count()
            print('Total:', total)

            for article in articles:
                kwargs = article.get_elasticsearch_kwargs()
                doc_dict = SearchIndex(boost=boost, **kwargs).to_dict(True)
                doc_dict['_id'] = article.get_elasticsearch_id()
                documents.append(doc_dict)
                print(value, 'of', total)
                value += 1
            print('*' * 10)

            # Index multiple documents
            bulk(connections.get_connection(), documents)
