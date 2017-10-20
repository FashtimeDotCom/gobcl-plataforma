from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.GovernmentStructureListView.as_view(),
        name='government_structure_list'
    ),
    url(
        r'^create/$',
        views.GovernmentStructureCreateView.as_view(),
        name='government_structure_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.GovernmentStructureDetailView.as_view(),
        name='government_structure_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.GovernmentStructureUpdateView.as_view(),
        name='government_structure_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.GovernmentStructureDeleteView.as_view(),
        name='government_structure_delete',
    ),
]
