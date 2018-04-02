from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views
from presidencies.views import PresidencyDetailView
from sociocultural_departments.views import SocioculturalDepartmentDetailView


urlpatterns = [
    url(
        r'^$',
        views.InstitutionListView.as_view(),
        name='institution_list'
    ),
    url(
        _(r'^presidency/$'),
        PresidencyDetailView.as_view(),
        name='presidency_detail'
    ),
    url(
        _(r'^sociocultural/$'),
        SocioculturalDepartmentDetailView.as_view(),
        name='sociocultural_department_detail'
    ),
]
