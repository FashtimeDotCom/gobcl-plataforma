from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.CampaignListView.as_view(),
        name='campaign_list'
    ),
    url(
        r'^create/$',
        views.CampaignCreateView.as_view(),
        name='campaign_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.CampaignDetailView.as_view(),
        name='campaign_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.CampaignUpdateView.as_view(),
        name='campaign_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.CampaignDeleteView.as_view(),
        name='campaign_delete',
    ),
]
