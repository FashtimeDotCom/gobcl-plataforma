from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.PresidencyListView.as_view(),
        name='presidency_list'
    ),
    url(
        r'^create/$',
        views.PresidencyCreateView.as_view(),
        name='presidency_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.PresidencyDetailView.as_view(),
        name='presidency_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.PresidencyUpdateView.as_view(),
        name='presidency_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.PresidencyDeleteView.as_view(),
        name='presidency_delete',
    ),
]
