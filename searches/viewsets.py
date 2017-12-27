import itertools

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import ArticleSerializer

from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig

from services.models import ChileAtiendeFile


class LimitOffsetPagination(LimitOffsetPagination):

    def get_limit(self, request):
        newsblog_config = NewsBlogConfig.objects.filter(
            namespace='aldryn_newsblog_default'
        ).values('paginate_by')

        default_limit = newsblog_config[0].get('paginate_by')

        return default_limit


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Article
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.model.objects.all().prefetch_related(
            'translations',
            'featured_image',
        ).select_related(
            'app_config',
            'featured_image',
        )


class ArticleSearchViewSet(ArticleViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # queryset = list(itertools.chain(
        #         ChileAtiendeFile.objects.all()[:10], Article.objects.all()[:10]
        #     )
        # )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super(ArticleSearchViewSet, self).get_queryset()

        self.query = self.request.GET.get('q', '')
        self.category_slug = self.request.GET.get('category_slug', '')

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
