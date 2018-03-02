from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
    url(
        _(r'^(?P<article_id>\d+)/$'),
        views.ArticleRedirectView.as_view(),
        name='article_redirect_view'
    ),
    url(
        _(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$'),
        views.ArticleDateRedirectView.as_view(),
        name='article_redirect_date_view'
    ),
]
