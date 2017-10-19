from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.InstitutionListView.as_view(),
        name='institution_list'
    ),
]
