from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.StreamDetailView.as_view(),
        name='stream_detail'
    ),
]
