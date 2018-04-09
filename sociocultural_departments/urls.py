from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^create/$',
        views.SocioculturalDepartmentCreateView.as_view(),
        name='sociocultural_department_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.SocioculturalDepartmentDetailView.as_view(),
        name='sociocultural_department_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.SocioculturalDepartmentUpdateView.as_view(),
        name='sociocultural_department_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.SocioculturalDepartmentDeleteView.as_view(),
        name='sociocultural_department_delete',
    ),
]
