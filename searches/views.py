# standard library
from itertools import chain

# django
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView

# models
from aldryn_newsblog.models import Article
from campaigns.models import Campaign
from ministries.models import Ministry
from ministries.models import PublicService
from presidencies.models import Presidency
from public_enterprises.models import PublicEnterprise
from public_servants.models import PublicServant
from regions.models import Region
from sociocultural_departments.models import SocioculturalDepartment
from links.models import FooterLink

from base.view_utils import clean_query_string

# chile atiende
from services.chile_atiende_client import File
from .elasticsearch.elasticsearch_client import ElasticSearchClient


class ArticleListView(ListView):
    model = Article
    template_name = 'search/search.pug'
    paginate_by = 25
    page_kwarg = 'p'

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('q', '')

        self.category_slug = request.GET.get('category_slug', '')

        return super(ArticleListView, self).get(request)

    def get_campaigns(self, **kwargs):
        if self.query:
            return Campaign.objects.active().translated(
                title__unaccent__icontains=self.query
            ).prefetch_related('translations')[:10]

        return []

    def get_chileatiende_files(self, **kwags):
        chile_atiende_file_client = File()

        # set the list as empty by default
        chile_atiende_files = []
        if self.request.GET.get('q'):
            if settings.CHILEATIENDE_ACCESS_TOKEN:
                chile_atiende_files = (
                    chile_atiende_file_client.parsed_list(query=self.query)
                )
        return chile_atiende_files

    def get_ministries(self, **kwargs):
        if self.query:
            ministries = Ministry.objects.by_government_structure(
                self.request.government_structure
            )
            ministry_ids = ministries.translated(
                name__unaccent__icontains=self.query
            ) | ministries.filter(
                minister__name__unaccent__icontains=self.query
            ) | ministries.filter(
                public_servants__name__unaccent__icontains=self.query
            )

            return Ministry.objects.filter(
                id__in=ministry_ids.values('id')
            ).prefetch_related(
                'translations'
            ).select_related(
                'minister'
            )

        return []

    def get_footer_links(self, **kwargs):
        if self.query and len(self.query) > 3:
            return FooterLink.objects.by_government_structure(
                self.request.government_structure
            ).filter(
                name__unaccent__icontains=self.query
            )

        return []

    def get_presidents(self, **kwargs):
        if self.query:
            presidency = Presidency.objects.filter(
                government_structure=self.request.government_structure
            )

            presidency_ids = presidency.filter(
                name__unaccent__icontains=self.query
            ) | presidency.translated(
                title__unaccent__icontains=self.query
            )

            return Presidency.objects.filter(
                id__in=presidency_ids.values('id')
            ).prefetch_related(
                'translations'
            )

        return []

    def get_public_enterprises(self, **kwargs):
        if self.query:
            return PublicEnterprise.objects.filter(
                government_structure=self.request.government_structure
            ).exclude(
                url=None
            ).translated(
                name__unaccent__icontains=self.query
            ).prefetch_related('translations')[:5]

        return []

    def get_public_servants(self, **kwargs):
        if self.query:
            return PublicServant.objects.filter(
                government_structure=self.request.government_structure
            ).filter(
                name__unaccent__icontains=self.query
            ).prefetch_related('translations')[:10]

        return []

    def get_public_services(self, **kwargs):
        if self.query:
            government_structure = self.request.government_structure
            return PublicService.objects.filter(
                ministry__government_structure=government_structure
            ).exclude(
                url=None
            ).translated(
                name__unaccent__icontains=self.query
            ).prefetch_related('translations')

        return []

    def get_regions(self, **kwargs):
        if self.query:
            regions = Region.objects.by_government_structure(
                self.request.government_structure
            )
            region_ids = regions.translated(
                name__unaccent__icontains=self.query
            ) | regions.filter(
                governor__name__unaccent__icontains=self.query
            ) | regions.filter(
                commune__name__unaccent__icontains=self.query
            )

            return Region.objects.filter(
                id__in=region_ids.values('id')
            ).prefetch_related(
                'translations'
            ).select_related(
                'governor'
            )

        return []

    def get_sociocultural_department(self, **kwargs):
        if self.query:
            sociocultural_department = SocioculturalDepartment.objects.filter(
                government_structure=self.request.government_structure
            )

            sociocultural_department_ids = sociocultural_department.filter(
                name__unaccent__icontains=self.query
            ) | sociocultural_department.translated(
                title__unaccent__icontains=self.query
            )

            return SocioculturalDepartment.objects.filter(
                id__in=sociocultural_department_ids.values('id')
            ).prefetch_related(
                'translations'
            )

        return []

    def get_foundations(self, **kwargs):
        if self.query:
            sociocultural_department = SocioculturalDepartment.objects.filter(
                government_structure=self.request.government_structure
            ).first()

            urls = sociocultural_department.urls.all()

            foundations = urls.filter(
                url=self.query,
            ) | urls.translated(
                name__unaccent__icontains=self.query,
            )
            return foundations

        return []

    def get_custom_results(self, **kwargs):
        if self.query:
            migration_keywords = [
                'migracion',
                'migración',
                'migrante',
                'amnistia',
                'amnistía',
                'extranjero',
                'extranjería',
                'extranjeria',
                'perdonazo',
                'migran',
                'migrar',
                'etranje',
            ]

            has_migration = any(n in self.query for n in migration_keywords)

            if has_migration:
                return [{
                    'get_absolute_url': 'https://www.gob.cl/nuevaleydemigracion/',
                    'name': 'Nueva Ley de Migración',
                    'description': (
                        'Conoce los fundamentos de la nueva reforma para '
                        'lograr una migración segura, ordenada y regular.'
                    ),
                    'title': 'https://www.gob.cl/nuevaleydemigracion/',
                }]

        return []

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)

        context['clean_query_string'] = clean_query_string(self.request)
        # Count the total list of objects
        context['count'] = self.count
        context['query'] = self.query

        return context

    def get_queryset(self):
        queryset = super(ArticleListView, self).get_queryset().published()

        if self.query:
            queryset = queryset.filter(
                Q(translations__title__unaccent__icontains=self.query) |
                Q(translations__lead_in__unaccent__icontains=self.query) |
                Q(translations__search_data__unaccent__icontains=self.query)
            ).distinct()

        if self.category_slug:
            queryset = queryset.filter(
                categories__translations__slug__icontains=self.category_slug
            ).distinct()

        queryset = list(
            chain(
                self.get_custom_results(),
                self.get_presidents(),
                self.get_sociocultural_department(),
                self.get_public_servants(),
                self.get_footer_links(),
                self.get_ministries(),
                self.get_foundations(),
                self.get_regions(),
                self.get_campaigns(),
                self.get_public_services(),
                self.get_public_enterprises(),
                queryset,
                self.get_chileatiende_files(),
            )
        )

        self.count = len(queryset)

        return queryset


class SearchTemplateView(ListView):
    template_name = 'search/search.pug'
    paginate_by = 25
    page_kwarg = 'p'

    def dispatch(self, request, *args, **kwargs):
        self.query = request.GET.get('q', '')
        self.replace_query = request.GET.get('replace') != 'keep'
        self.category_slug = request.GET.get('category_slug', '')
        # search in chile atiende
        self.chile_atiende_results = self.get_chileatiende_files()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clean_query_string'] = clean_query_string(self.request)
        context['query'] = self.query
        context['count'] = self.count
        context['suggest_text'] = self.suggest_text
        context['replace_query'] = self.replace_query
        context['chile_atiende_results'] = self.chile_atiende_results

        return context

    def get_suggest_text(self, response):
        self.suggest_text = None
        try:
            suggestions = response.suggest
            suggestion_list = []

            for suggest in suggestions:
                try:
                    suggestion_list.append(
                        (
                            suggestions[suggest][0]['options'][0]['text'],
                            suggestions[suggest][0]['options'][0]['score']
                        )
                    )
                except (IndexError, KeyError):
                    pass

            if len(suggestion_list) > 0:
                self.suggest_text = max(suggestion_list, key=lambda x: x[1])[0]

        except AttributeError:
            pass

    def get_chileatiende_files(self, **kwags):
        chile_atiende_file_client = File()

        # set the list as empty by default
        chile_atiende_files = []
        if settings.CHILEATIENDE_ACCESS_TOKEN:
            chile_atiende_files = (
                chile_atiende_file_client.parsed_list(query=self.query)
            )
        return chile_atiende_files[:3]

    def get_search_response(self, query):
        elastic_search_client = ElasticSearchClient(
            query,
            self.request.LANGUAGE_CODE
        )
        response = elastic_search_client.execute()
        self.count = len(response)

        return response

    def get_queryset(self):
        # search in database
        response = self.get_search_response(self.query)
        self.get_suggest_text(response)

        if self.replace_query:
            if self.count < settings.MIN_LENGTH_REPLACE_SEARCH and self.suggest_text is not None:
                response = self.get_search_response(self.suggest_text)
            else:
                self.suggest_text = None

        return response
