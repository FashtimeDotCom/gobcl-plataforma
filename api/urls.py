from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from regions.viewsets import CommuneViewSet
from searches.viewsets import ArticleViewSet
from searches.viewsets import ArticleSearchViewSet

router = DefaultRouter()
router.register(r'communes', CommuneViewSet, 'commune')
router.register(r'articles', ArticleViewSet, 'article')
router.register(r'search', ArticleSearchViewSet, 'article')

urlpatterns = [
    url(r'^', include(router.urls)),
]
