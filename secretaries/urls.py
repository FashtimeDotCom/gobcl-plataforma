from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.SecretaryListView.as_view(),
        name='secretary_list'
    ),
    url(
        r'^create/$',
        views.SecretaryCreateView.as_view(),
        name='secretary_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.SecretaryDetailView.as_view(),
        name='secretary_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.SecretaryUpdateView.as_view(),
        name='secretary_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.SecretaryDeleteView.as_view(),
        name='secretary_delete',
    ),
]
