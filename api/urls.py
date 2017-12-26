from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from regions.viewsets import CommuneViewSet
from searches.viewsets import ArticleViewSet

router = DefaultRouter()
router.register(r'communes', CommuneViewSet, 'commune')
router.register(r'articles', ArticleViewSet, 'article')

urlpatterns = [
    url(r'^', include(router.urls)),
]
