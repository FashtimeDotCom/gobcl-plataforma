# django
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        r'^$',
        views.ArticleListView.as_view(),
        name='article_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.ArticleDetailView.as_view(),
        name='article_detail'
    ),
    url(
        r'^(?P<slug>[\w-]+)/publish/$',
        views.ArticlePublishView.as_view(),
        name='article_publish'
    ),
    url(
        r'^(?P<slug>[\w-]+)/unpublish/$',
        views.ArticleUnpublishView.as_view(),
        name='article_unpublish'
    ),
    url(
        _(r'^category/(?P<category>\w[-\w]*)/$'),
        views.CategoryArticleList.as_view(),
        name='article-list-by-category'
    ),
]
