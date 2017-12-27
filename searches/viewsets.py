import itertools
from collections import OrderedDict

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.pagination import _positive_int

from .serializers import ArticleSerializer
from services.serializers import ChileAtiendeFileSerializer

from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig

from services.models import ChileAtiendeFile


class LimitOffsetPagination(LimitOffsetPagination):

    def get_limit(self, request):

        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        newsblog_config = NewsBlogConfig.objects.filter(
            namespace='aldryn_newsblog_default'
        ).values('paginate_by')

        default_limit = newsblog_config[0].get('paginate_by')

        return default_limit

    def get_current_language(self):
        return self.request.LANGUAGE_CODE

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('current_language', self.get_current_language()),
            ('results', data),
        ]))


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Article
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        queryset = self.model.objects.all().prefetch_related(
            'translations',
            'featured_image',
        ).select_related(
            'app_config',
            'featured_image',
        )

        self.category_slug = self.request.GET.get('category_slug', '')

        if self.category_slug:
            queryset = queryset.filter(
                categories__translations__slug__icontains=self.category_slug
            ).distinct()

        return queryset


class ArticleSearchViewSet(ArticleViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super(ArticleSearchViewSet, self).get_queryset()
        querysetfile = ChileAtiendeFile.objects.all()

        self.query = self.request.GET.get('q', '')

        if self.query:
            queryset = queryset.filter(
                Q(translations__title__unaccent__icontains=self.query) |
                Q(translations__lead_in__unaccent__icontains=self.query) |
                Q(translations__search_data__unaccent__icontains=self.query)
            ).distinct()

            querysetfile = querysetfile.filter(
                Q(service__name__icontains=self.query) |
                Q(title__icontains=self.query) |
                Q(objective__icontains=self.query)
            ).distinct()
        
        queryset = list(itertools.chain(
                querysetfile, queryset
            )
        )

        return queryset
