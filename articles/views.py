# -*- coding: utf-8 -*-
""" Views for the articles application. """
# standard library

# django
from django.views.generic import ListView

# models
from .models import Article

# views
from base.views import BaseDetailView
from parler.views import TranslatableSlugMixin


class ArticleListView(ListView):
    """
    View for displaying a list of articles.
    """
    model = Article
    template_name = 'articles/article_list.pug'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        queryset = super(ArticleListView, self).get_queryset()
        return queryset.exclude(is_featured=True)


class ArticleDetailView(TranslatableSlugMixin, BaseDetailView):
    """
    A view for displaying a single campaign
    """
    model = Article
    template_name = 'articles/article_detail.pug'
    permission_required = 'campaigns.view_campaign'
