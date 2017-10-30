from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.LinkListView.as_view(),
        name='link_list'
    ),
    url(
        r'^create/$',
        views.LinkCreateView.as_view(),
        name='link_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.LinkDetailView.as_view(),
        name='link_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.LinkUpdateView.as_view(),
        name='link_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.LinkDeleteView.as_view(),
        name='link_delete',
    ),
]
