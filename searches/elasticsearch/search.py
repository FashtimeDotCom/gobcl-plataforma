import re

from abc import ABCMeta, abstractmethod

from django.utils.formats import date_format

from elasticsearch_dsl import IndexTemplate


def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


class ISearchMixin(metaclass=ABCMeta):
    languages = ('es', 'en',)

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def indexing(self):
        pass

    def get_name(self):
        if hasattr(self.obj, 'name'):
            return self.obj.name
        else:
            return ''

    def get_categories(self):
        if hasattr(self.obj, 'categories'):
            categories = self.obj.categories.values_list(
                'translations__name',
                flat=True
            )
            return ', '.join(categories)
        return ''

    def get_categories_slug(self):
        if hasattr(self.obj, 'categories'):
            categories = self.obj.categories.values_list(
                'translations__slug',
                flat=True
            )
            return ', '.join(categories)
        return ''

    def get_description(self):
        if hasattr(self.obj, 'description'):
            return remove_tags(self.obj.description)
        elif hasattr(self.obj, 'lead_in'):
            return remove_tags(self.obj.lead_in)
        else:
            return ''

    def get_language_code(self):
        if hasattr(self.obj, 'language_code'):
            return self.obj.language_code
        else:
            return 'ALL'

    def get_lead_in(self):
        if hasattr(self.obj, 'lead_in'):
            return remove_tags(self.obj.lead_in)
        else:
            return ''

    def get_detail(self):
        if hasattr(self.obj, 'publishing_date'):
            return date_format(self.obj.publishing_date)

        elif hasattr(self.obj, 'charge'):
            return self.obj.charge

        elif hasattr(self.obj, 'title'):
            return self.obj.title

        elif hasattr(self.obj, 'minister'):
            return self.obj.minister.name

        elif hasattr(self.obj, 'governor'):
            return self.obj.governor.name

        elif hasattr(self.obj, 'external_url'):
            return self.obj.external_url

        elif hasattr(self.obj, 'url'):
            return self.obj.url

        else:
            return ''

    def get_url(self):
        return self.obj.get_absolute_url()

    def get_tags(self):
        if hasattr(self.obj, 'tags'):
            tags = self.obj.tags.values_list('name', flat=True)
            return ', '.join(tags)
        else:
            return ''

    def get_title(self):
        if hasattr(self.obj, 'title'):
            return self.obj.title
        else:
            return ''

    def get_index(self):
        searches = IndexTemplate('search', 'search-*')

        searches.settings(
            number_of_shards=1,
            number_of_replicas=0
        )

        return searches

    def get_boost(self):
        return self.boost

    def index_obj(self):
        obj = self.document(
            name=self.get_name(),
            title=self.get_title(),
            description=self.get_description(),
            language_code=self.get_language_code(),
            url=self.get_url(),
            lead_in=self.get_lead_in(),
            detail=self.get_detail(),
            tags=self.get_tags(),
            categories=self.get_categories(),
            categories_slug=self.get_categories_slug(),
            boost=self.get_boost(),
        )
        obj.save()


class ISearchObj(ISearchMixin):

    def __init__(self, obj, document, boost=0, *args, **kwargs):
        self.obj = obj
        self.document = document
        self.boost = boost

    def indexing(self):
        self.index_obj()


class ISearch(ISearchMixin):

    def __init__(self, queryset, document, boost=0, *args, **kwargs):
        self.queryset = queryset
        self.document = document
        self.boost = boost

    def index_queryset(self):
        for obj in self.queryset:
            self.obj = obj
            self.index_obj()

    def index_queryset_with_language(self):
        for language in self.languages:
            self.queryset = self.queryset.language(language)
            self.index_queryset()

    def indexing(self):
        if hasattr(self.queryset.model, 'translations'):
            self.index_queryset_with_language()
        else:
            self.index_queryset()
