from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.ServiceListView.as_view(),
        name='service_list'
    ),
    url(
        r'^search/$',
        views.FileSearchJson.as_view(),
        name='file_list_json'
    ),
]
