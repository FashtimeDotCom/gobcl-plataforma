from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from regions.viewsets import CommuneViewSet

router = DefaultRouter()
router.register(r'communes', CommuneViewSet, 'commune')

urlpatterns = [
    url(r'^', include(router.urls)),
]
