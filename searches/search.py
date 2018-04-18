from django.utils.translation import activate
from django.utils.formats import date_format

from .elasticsearch_config import get_elasticsearch_url

from elasticsearch_dsl import DocType
from elasticsearch_dsl import Text
from elasticsearch_dsl import Index, IndexTemplate
from elasticsearch_dsl import connections
from elasticsearch_dsl import analyzer
from elasticsearch_dsl import Keyword

# models
from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from links.models import FooterLink
from campaigns.models import Campaign
from ministries.models import PublicService
from presidencies.models import Presidency
from articles.models import Article
from public_servants.models import PublicServant


connections.create_connection(
    hosts=[get_elasticsearch_url()],
    timeout=20
)

government_structure = GovernmentStructure.get_government()

html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    filter=['standard', 'lowercase', 'stop', 'snowball'],
    char_filter=['html_strip']
)


class ISearch:

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj

    def get_index(self):
        searches = IndexTemplate('search', 'search-*')

        searches.settings(
            number_of_shards=1,
            number_of_replicas=0
        )

        return searches

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
            return self.obj.description
        elif hasattr(self.obj, 'lead_in'):
            return self.obj.lead_in
        else:
            return ''

    def get_language_code(self):
        if hasattr(self.obj, 'language_code'):
            return self.obj.language_code
        else:
            return 'ALL'

    def get_lead_in(self):
        if hasattr(self.obj, 'lead_in'):
            return self.obj.lead_in
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

    def indexing(self):
        obj = SearchIndex(
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
        )
        obj.save()


class SearchIndex(DocType):
    name = Text()
    title = Text()
    description = Text()
    language_code = Text()
    url = Text()
    lead_in = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )
    detail = Text()
    tags = Text()
    categories = Text()
    categories_slug = Text()
    languages = ('es', 'en',)

    class Meta:
        index = 'searches'

    @classmethod
    def index_ministries(cls):
        for language in cls.languages:
            activate(language)
            ministries = Ministry.objects.translated(
                name__isnull=False,
            ).by_government_structure(
                government_structure
            )
            for ministry in ministries:
                search_index = ISearch(ministry)
                search_index.indexing()

    @classmethod
    def index_footer_link(cls):
        footer_links = FooterLink.objects.by_government_structure(
            government_structure
        )
        for footer_link in footer_links:
            search_index = ISearch(footer_link)
            search_index.indexing()

    @classmethod
    def index_presidencies(cls):
        for language in cls.languages:
            activate(language)
            presidencies = Presidency.objects.filter(
                government_structure=government_structure
            )
            for presidency in presidencies:
                search_index = ISearch(presidency)
                search_index.indexing()

    @classmethod
    def index_articles(cls):
        for language in cls.languages:
            activate(language)
            articles = Article.objects.translated(
                title__isnull=False,
            ).filter(
                is_draft=False,
            )[:10]
            for article in articles:
                search_index = ISearch(article)
                search_index.indexing()

    @classmethod
    def index_campaigns(cls):
        for language in cls.languages:
            activate(language)
            campaigns = Campaign.objects.translated(
                title__isnull=False,
            )
            for campaign in campaigns:
                search_index = ISearch(campaign)
                search_index.indexing()

    @classmethod
    def index_public_services(cls):
        for language in cls.languages:
            activate(language)
            public_services = PublicService.objects.translated(
                name__isnull=False,
            ).filter(
                ministry__government_structure=government_structure,
            )
            for public_service in public_services:
                search_index = ISearch(public_service)
                search_index.indexing()

    @classmethod
    def index_public_servant(cls):
        for language in cls.languages:
            activate(language)
            public_servants = PublicServant.objects.filter(
                government_structure=government_structure
            ).translated(
                charge__isnull=False,
            )
            for public_servant in public_servants:
                search_index = ISearch(public_servant)
                search_index.indexing()

    @classmethod
    def bulk_indexing(cls):
        cls.init()
        cls.index_public_servant()
        cls.index_presidencies()
        cls.index_articles()
        cls.index_public_services()
        cls.index_campaigns()
        cls.index_footer_link()
        cls.index_ministries()

    @classmethod
    def delete(cls):
        try:
            return Index('searches').delete()
        except:
            pass

    @classmethod
    def rebuild(cls):
        cls.delete()
        cls.bulk_indexing()
