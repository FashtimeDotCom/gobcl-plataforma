import itertools
from collections import OrderedDict

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.pagination import _positive_int
from rest_framework.utils.urls import remove_query_param, replace_query_param

from .serializers import ArticleSerializer
from services.serializers import ChileAtiendeFileSerializer

from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig

from services.models import ChileAtiendeFile


class LimitOffsetPagination(LimitOffsetPagination):

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)

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
        self.query = self.request.GET.get('q', '')

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


class ArticleSearchViewSet(ArticleViewSet):

    def get_queryset(self):
        queryset = super(ArticleSearchViewSet, self).get_queryset()
        querysetfile = ChileAtiendeFile.objects.all()

        if self.query:
            querysetfile = querysetfile.filter(
                Q(service__name__unaccent__icontains=self.query) |
                Q(title__unaccent__icontains=self.query) |
                Q(objective__unaccent__icontains=self.query)
            ).distinct()
        
        queryset = list(itertools.chain(
                querysetfile, queryset
            )
        )

        return queryset
