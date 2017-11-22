from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.ServiceListView.as_view(),
        name='service_list'
    ),
    url(
        r'^create/$',
        views.ServiceCreateView.as_view(),
        name='service_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.ServiceDetailView.as_view(),
        name='service_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.ServiceUpdateView.as_view(),
        name='service_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.ServiceDeleteView.as_view(),
        name='service_delete',
    ),
]
