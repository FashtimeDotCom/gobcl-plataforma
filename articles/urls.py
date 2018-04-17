from django.conf.urls import url

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
]
