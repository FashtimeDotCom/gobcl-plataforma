from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.PublicCompanyListView.as_view(),
        name='public_company_list'
    ),
    url(
        r'^create/$',
        views.PublicCompanyCreateView.as_view(),
        name='public_company_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.PublicCompanyDetailView.as_view(),
        name='public_company_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.PublicCompanyUpdateView.as_view(),
        name='public_company_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.PublicCompanyDeleteView.as_view(),
        name='public_company_delete',
    ),
]
