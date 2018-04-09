# standard library
#
# django
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView

from aldryn_newsblog.models import Article
from campaigns.models import Campaign
from ministries.models import Ministry
from ministries.models import PublicService
from presidencies.models import Presidency
from public_enterprises.models import PublicEnterprise
from public_servants.models import PublicServant
from regions.models import Region

# chile atiende
from services.chile_atiende_client import File


class ArticleListView(ListView):
    model = Article
    template_name = 'search/search.pug'
    paginate_by = 25

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
        chileatiende_files = []
        if self.request.GET.get('q'):
            if settings.CHILEATIENDE_ACCESS_TOKEN:
                chile_atiende_files = (
                    chile_atiende_file_client.parsed_list(query=self.query)
                )
        return chileatiende_files

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
                'etranje',
            ]

            has_migration = any(n in self.query for n in migration_keywords)

            if has_migration:
                return [{
                    'url': 'https://www.gob.cl/nuevaleydemigracion/',
                    'name': 'Nueva Ley de Migración',
                    'description': (
                        'Conoce los fundamentos de la nueva reforma para '
                        'lograr una migración segura, ordenada y regular.'
                    ),
                }]

        return []

    def get_presidents(self, **kwargs):
        if self.query:
            presidency = Presidency.objects.filter(
                government_structure=self.request.government_structure
            )

            presidency_ids = presidency.filter(
                name__unaccent__icontains=self.query
            ) | presidency.translated (
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
            ).prefetch_related('translations')[:5]

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

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)

        context['campaigns'] = self.get_campaigns()

        # obtain chile atiende files
        context['chile_atiende_files_json'] = self.get_chileatiende_files()

        context['ministries'] = self.get_ministries()

        context['public_enterprises'] = self.get_public_enterprises()

        context['public_servants'] = self.get_public_servants()

        context['public_services'] = self.get_public_services()

        context['custom_results'] = self.get_custom_results()

        context['presidents'] = self.get_presidents()

        context['regions'] = self.get_regions()

        # Count the total list of objects
        context['count'] = (
            context['object_list'].count() +
            len(context['campaigns']) +
            len(context['chile_atiende_files_json']) +
            len(context['custom_results']) +
            len(context['ministries']) +
            len(context['presidents']) +
            len(context['public_enterprises']) +
            len(context['public_servants']) +
            len(context['public_services']) +
            len(context['regions'])
        )

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

        return queryset
