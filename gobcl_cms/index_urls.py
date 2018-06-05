from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.IndexTemplateView.as_view(),
        name='home'
    ),
]
