from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import ArticleSerializer

from aldryn_newsblog.models import Article


class LimitOffsetPagination(LimitOffsetPagination):
    default_limit = 12


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Article
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination
    # filter_fields = ('region',)

    def get_queryset(self):
        return self.model.objects.filter().prefetch_related(
            'translations',
        ).select_related(
            'app_config',
        )
