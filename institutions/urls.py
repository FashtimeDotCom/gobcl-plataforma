from django.conf.urls import url

from . import views
from presidencies.views import PresidencyDetailView


urlpatterns = [
    url(
        r'^$',
        views.InstitutionListView.as_view(),
        name='institution_list'
    ),
    url(
        r'^presidency/$',
        PresidencyDetailView.as_view(),
        name='presidency_detail'
    ),
]
