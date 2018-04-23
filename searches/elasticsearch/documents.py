from django.utils.translation import activate
from django.utils.timezone import now

from .elasticsearch_config import get_elasticsearch_url

from elasticsearch.exceptions import NotFoundError

from elasticsearch_dsl import DocType
from elasticsearch_dsl import Text
from elasticsearch_dsl import Index
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

from .search import ISearch, ISearchObj

connections.create_connection(
    hosts=[get_elasticsearch_url()],
    timeout=20
)


government_structure = GovernmentStructure.get_government()

html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    # filter=['standard', 'lowercase', 'stop', 'snowball'],
    char_filter=['html_strip']
)


class SearchIndex(DocType):
    name = Text(store=True)
    title = Text(store=True)
    description = Text(
        analyzer=html_strip,
        store=True
    )
    language_code = Text()
    url = Text()
    lead_in = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()},
        store=True
    )
    detail = Text(store=True)
    tags = Text()
    categories = Text()
    categories_slug = Text()

    class Meta:
        index = 'searches'

    @classmethod
    def index_ministries(cls):
        ministries = Ministry.objects.translated(
            name__isnull=False,
        ).by_government_structure(
            government_structure
        )
        ISearch(ministries, cls).indexing()

    @classmethod
    def index_footer_link(cls):
        footer_links = FooterLink.objects.by_government_structure(
            government_structure
        )
        ISearch(footer_links, cls).indexing()

    @classmethod
    def index_presidencies(cls):
        presidencies = Presidency.objects.filter(
            government_structure=government_structure
        )
        ISearch(presidencies, cls).indexing()

    @classmethod
    def index_articles(cls):
        languages = ('es', 'en')
        for language in languages:
            activate(language)
            articles = Article.objects.translated(
                title__isnull=False,
            ).filter(
                publishing_date__lte=now(),
                is_draft=False,
            )
            for article in articles:
                print(article.title, article.pk)
                search_index = ISearchObj(article, cls)
                search_index.indexing()

    @classmethod
    def index_campaigns(cls):
        campaigns = Campaign.objects.translated(
            title__isnull=False,
        )
        ISearch(campaigns, cls).indexing()

    @classmethod
    def index_public_services(cls):
        public_services = PublicService.objects.translated(
            name__isnull=False,
        ).filter(
            ministry__government_structure=government_structure,
        )
        ISearch(public_services, cls).indexing()

    @classmethod
    def index_public_servant(cls):
        public_servants = PublicServant.objects.filter(
            government_structure=government_structure
        ).translated(
            charge__isnull=False,
        )
        ISearch(public_servants, cls).indexing()

    @classmethod
    def bulk_indexing(cls):
        cls.init()

        cls.index_articles()
        activate('es')
        print('public servant')
        cls.index_public_servant()
        print('public presidency')
        cls.index_presidencies()
        print('public articles')
        print('public public services')
        cls.index_public_services()
        print('campaigns')
        cls.index_campaigns()
        print('foote rlinks')
        cls.index_footer_link()
        print('ministries')
        cls.index_ministries()

    @classmethod
    def delete(cls):
        try:
            return Index('searches').delete()
        except NotFoundError:
            pass

    @classmethod
    def rebuild(cls):
        cls.delete()
        cls.bulk_indexing()
