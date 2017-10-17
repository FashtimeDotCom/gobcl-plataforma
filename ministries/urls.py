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
]
