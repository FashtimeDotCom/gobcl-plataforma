from django.conf.urls import url

from . import views


urlpatterns = [
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
        r'^(?P<pk>[\d]+)/$',
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
