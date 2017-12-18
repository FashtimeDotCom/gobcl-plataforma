from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.ContingencyListView.as_view(),
        name='contingency_list'
    ),
    url(
        r'^create/$',
        views.ContingencyCreateView.as_view(),
        name='contingency_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.ContingencyDetailView.as_view(),
        name='contingency_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.ContingencyUpdateView.as_view(),
        name='contingency_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.ContingencyDeleteView.as_view(),
        name='contingency_delete',
    ),
]
