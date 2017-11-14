from django.views.generic import ListView
from django.db.models import Q

from aldryn_newsblog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'search/search.pug'
    paginate_by = 25

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('q', '')

        self.category_slug = request.GET.get('q', '')

        return super(ArticleListView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['query'] = self.query
        return context

    def get_queryset(self):
        queryset = super(ArticleListView, self).get_queryset().published()

        if self.query:
            queryset = queryset.filter(
                Q(translations__title__icontains=self.query) |
                Q(translations__lead_in__icontains=self.query) |
                Q(translations__search_data__icontains=self.query)
            ).distinct()

        if self.category_slug:
            queryset = queryset.filter(
                categories__slug=self.category_slug
            ).distinct()

        return queryset
