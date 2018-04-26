from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from regions.viewsets import CommuneViewSet
from searches.viewsets import ArticleViewSet
from searches.viewsets import SearchList
from streams.viewsets import StreamViewSet

router = DefaultRouter()
router.register(r'communes', CommuneViewSet, 'commune')
router.register(r'articles', ArticleViewSet, 'article')
router.register(r'search', SearchList, 'search')
router.register(r'streams', StreamViewSet, 'stream')

urlpatterns = [
    url(r'^', include(router.urls)),
]
