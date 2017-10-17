from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.GovernmentListView.as_view(),
        name='government_list'
    ),
    url(
        r'^create/$',
        views.GovernmentCreateView.as_view(),
        name='government_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.GovernmentDetailView.as_view(),
        name='government_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.GovernmentUpdateView.as_view(),
        name='government_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.GovernmentDeleteView.as_view(),
        name='government_delete',
    ),
]
