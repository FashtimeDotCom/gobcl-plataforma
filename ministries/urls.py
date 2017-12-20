from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.MinistryListView.as_view(),
        name='ministry_list'
    ),
    url(
        r'^create/$',
        views.MinistryCreateView.as_view(),
        name='ministry_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.MinistryDetailView.as_view(),
        name='ministry_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.MinistryUpdateView.as_view(),
        name='ministry_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.MinistryDeleteView.as_view(),
        name='ministry_delete',
    ),
    url(
        r'^public-service$',
        views.PublicServiceListView.as_view(),
        name='publicservice_list'
    ),
    url(
        r'^public-service/create/$',
        views.PublicServiceCreateView.as_view(),
        name='publicservice_create'
    ),
    url(
        r'^public-service/(?P<pk>[\d]+)/update/$',
        views.PublicServiceUpdateView.as_view(),
        name='publicservice_update'
    ),
    url(
        r'^public-service/(?P<pk>[\d]+)/delete/$',
        views.PublicServiceDeleteView.as_view(),
        name='publicservice_delete',
    ),
]
