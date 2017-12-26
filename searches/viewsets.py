from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import ArticleSerializer

from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig


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
