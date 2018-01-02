from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
    url(
        _(r'^(?P<pk>\d+)/change/$'),
        views.ArticleRelatedUpdateView.as_view(),
        name='article_related_update_view'
    ),
]
