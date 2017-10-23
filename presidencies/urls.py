from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.PresidencyDetailView.as_view(),
        name='presidency_detail'
    ),
]
