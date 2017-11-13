from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.PublicEnterpriseListView.as_view(),
        name='public_enterprise_list'
    ),
    url(
        r'^create/$',
        views.PublicEnterpriseCreateView.as_view(),
        name='public_enterprise_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.PublicEnterpriseDetailView.as_view(),
        name='public_enterprise_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.PublicEnterpriseUpdateView.as_view(),
        name='public_enterprise_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.PublicEnterpriseDeleteView.as_view(),
        name='public_enterprise_delete',
    ),
]
