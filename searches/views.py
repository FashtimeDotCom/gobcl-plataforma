# standard library
import json

# django
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView

from aldryn_newsblog.models import Article

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

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)

        # obinta chile atiende files
        chile_atiende_file_client = File()

        # set the list as empty by default
        context['chile_atiende_files_json'] = []
        if self.request.GET.get('q'):
            if settings.CHILEATIENDE_ACCESS_TOKEN:
                response = chile_atiende_file_client.list(query=self.query)

                if response.status_code == 200:
                    context['chile_atiende_files_json'] = json.loads(
                        response.text
                    )['fichas']['items']

        # Count the total list of objects
        context['count'] = (
            context['object_list'].count() +
            len(context['chile_atiende_files_json'])
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
