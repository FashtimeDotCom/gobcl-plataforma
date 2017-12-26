from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^(?P<region_slug>[\w-]+)/communes/$',
        views.CommuneListView.as_view(),
        name='commune_list'
    ),
    url(
        r'^(?P<region_slug>[\w-]+)/communes/create/$',
        views.CommuneCreateView.as_view(),
        name='commune_create'
    ),
    url(
        r'^(?P<region_slug>[\w-]+)/communes/(?P<pk>[\d]+)/update/$',
        views.CommuneUpdateView.as_view(),
        name='commune_update'
    ),
    url(
        r'^(?P<region_slug>[\w-]+)/communes/(?P<pk>[\d]+)/delete/$',
        views.CommuneDeleteView.as_view(),
        name='commune_delete',
    ),
    url(
        r'^$',
        views.RegionListView.as_view(),
        name='region_list'
    ),
    url(
        r'^create/$',
        views.RegionCreateView.as_view(),
        name='region_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.RegionDetailView.as_view(),
        name='region_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.RegionUpdateView.as_view(),
        name='region_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.RegionDeleteView.as_view(),
        name='region_delete',
    ),
]
