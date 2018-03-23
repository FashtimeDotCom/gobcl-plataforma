# -*- coding: utf-8 -*-
""" Models for the government_structures application. """
# standard library
import copy

from threading import Thread

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate

# models
from base.models import BaseModel


class GovernmentStructure(BaseModel):
    publication_date = models.DateTimeField(
        _('publication date'),
        unique=True,
    )
    current_government = models.BooleanField(
        _('current government'),
        default=False,
    )
    archive_news = models.BooleanField(
        _('archive news'),
        default=False,
        help_text='archive government news',
    )

    class Meta:
        ordering = ('-publication_date',)
        verbose_name = _('government structure')
        verbose_name_plural = _('government structures')
        permissions = (
            ('view_government_structure', _('Can view government structures')),
        )

    def __init__(self, *args, **kwargs):
        super(GovernmentStructure, self).__init__(*args, **kwargs)
        self.previous_archive_news = self.archive_news

    def __str__(self):
        return '{}'.format(self.publication_date)

    def save(self, **kwargs):
        # Make sure the default government are unique
        if self.current_government:
            GovernmentStructure.objects.filter(
                current_government=True,
            ).update(
                current_government=False,
            )
        if self.archive_news and not self.previous_archive_news:
            self._archive_news()
        super(GovernmentStructure, self).save(**kwargs)

    @classmethod
    def get_government(cls, date=None):
        if not date:
            return cls.objects.get_or_none(current_government=True)

    def _archive_news(self):
        t = Thread(target=self._archive_news2)
        t.start()

    def _archive_news2(self):
        from aldryn_newsblog.models import Article
        from taggit.models import Tag

        tag = Tag.objects.get_or_create(name='archivo')[0]

        next_government_structure = self.get_next_by_publication_date()

        activate('es')
        articles = Article.objects.exclude(tags=tag).filter(
            publishing_date__gte=self.publication_date,
        )
        if next_government_structure:
            articles = articles.filter(
                publishing_date__lte=next_government_structure.publication_date
            )

        for article in articles:
            if article.title.startswith('[ARCHIVO]'):
                print('se saltó')
                continue

            article.title = '[ARCHIVO] ' + article.title
            article.tags.add(tag)
            article.save()
            print(article.title)

        tag = Tag.objects.get_or_create(name='archive')[0]
        activate('en')
        articles = Article.objects.exclude(tags=tag).filter(
            publishing_date__gte=self.publication_date,
        )
        if next_government_structure:
            articles = articles.filter(
                publishing_date__lte=next_government_structure.publication_date
            )

        for article in articles:
            if article.title.startswith('[ARCHIVE]') or article.title.startswith('[ARCHIVO]'):
                print('se saltó')
                continue

            article.title = '[ARCHIVE] ' + article.title
            article.tags.add(tag)
            article.save()
            print(article.title)

    def duplicate(self, date, with_public_servants=True):
        from ministries.models import Ministry
        from public_servants.models import PublicServant

        government_structures = GovernmentStructure.objects.filter(
            publication_date=date)
        if government_structures.exists():
            return

        government_structure = copy.copy(self)
        government_structure.id = None
        government_structure.current_government = False
        government_structure.publication_date = date
        government_structure.save()

        field_map = self._meta.fields_map

        children_government_structure = {
            'publicservant': field_map.get('publicservant'),
            'ministry': field_map.get('ministry'),
            'region': field_map.get('region'),
            'publicenterprise': field_map.get('publicenterprise'),
            'footerlink': field_map.get('footerlink'),
            'presidency': field_map.get('presidency'),
        }

        for child in children_government_structure:
            field = children_government_structure.get(child)

            if not field:
                continue

            if not with_public_servants:
                if field.name == 'publicservant':
                    continue

            model = field.related_model
            objects = model.objects.filter(government_structure=self)
            for obj in objects:
                new_obj = copy.copy(obj)

                # Check for and copy translations in model
                if hasattr(new_obj, 'translations'):
                    translations = copy.copy(new_obj.translations.all())
                else:
                    translations = None

                new_obj.id = None
                new_obj.government_structure = government_structure
                new_obj.save()

                if translations:
                    for translation in translations:
                        translation.id = None
                        translation.master_id = new_obj.id
                        translation.save()

                if child == 'ministry':

                    # copy public services
                    for public_service in obj.publicservice_set.all():
                        new_public_service = copy.copy(public_service)
                        new_public_service.id = None
                        new_public_service.ministry_id = new_obj.id
                        new_public_service.save()

                        translations = copy.copy(
                            public_service.translations.all()
                        )

                        for translation in translations:
                            translation.id = None
                            translation.master_id = new_public_service.id
                            translation.save()

                    if not with_public_servants:
                        new_obj.minister = None
                        new_obj.public_servants.clear()
                        new_obj.save()
                        continue

                    minister = PublicServant.objects.filter(
                        government_structure=government_structure
                    ).filter(name=obj.minister.name).first()
                    public_servants = PublicServant.objects.filter(
                        government_structure=government_structure,
                        name__in=obj.public_servants.values_list(
                            'name', flat=True)
                    )
                    new_obj.minister = minister
                    new_obj.public_servants.add(*public_servants)
                    new_obj.save()

                if child == 'region':
                    # copy communes

                    for commune in obj.commune_set.all():
                        new_commune = copy.copy(commune)
                        new_commune.id = None
                        new_commune.region_id = new_obj.id
                        new_commune.save()

                    if not with_public_servants:
                        new_obj.governor = None
                        new_obj.save()
                        continue

                    governor = PublicServant.objects.filter(
                        government_structure=government_structure
                    ).filter(name=obj.governor.name).first()

                    new_obj.governor = governor
                    new_obj.save()

                if child == 'publicenterprise':
                    ministries = Ministry.objects.filter(
                        government_structure=government_structure,
                    ).translated(
                        name__in=obj.ministries.values_list(
                            'translations__name', flat=True)
                    )
                    new_obj.ministries.add(*ministries)
                    new_obj.save()

                if child == 'presidency':

                    # Blank presidency
                    new_obj.name = 'Nuevo mandatario de la República'
                    new_obj.photo = None
                    new_obj.twitter = ''
                    new_obj.url = ''

                    for translation in new_obj.translations.all():
                        translation.title = ''
                        translation.description = ''
                        translation.save()

                    urls = []
                    for link in obj.urls.all():
                        new_link = copy.copy(link)
                        new_link.id = None
                        new_link.url = 'https://www.gob.cl/'
                        new_link.save()

                        translations = copy.copy(
                            link.translations.all()
                        )

                        for translation in translations:
                            translation.id = None
                            translation.name = 'ingrese texto relevante'
                            translation.description = 'ingrese texto relevante'
                            translation.master_id = new_link.id
                            translation.save()
                        urls.append(new_link)

                    new_obj.urls.add(*urls)
                    new_obj.save()

        return government_structure
