from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.PublicServantListView.as_view(),
        name='public_servant_list'
    ),
    url(
        r'^create/$',
        views.PublicServantCreateView.as_view(),
        name='public_servant_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.PublicServantDetailView.as_view(),
        name='public_servant_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.PublicServantUpdateView.as_view(),
        name='public_servant_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.PublicServantDeleteView.as_view(),
        name='public_servant_delete',
    ),
]
