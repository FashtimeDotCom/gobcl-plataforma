# -*- coding: utf-8 -*-
""" Views for the Article application. """
# standard library

# django
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin

# base
from django.views.generic import FormView
from django.shortcuts import get_object_or_404

# models
from aldryn_newsblog.models import Article

# forms
from .forms import ArticleForm

# newsblog
from aldryn_newsblog.views import ArticleList


def get_queryset(self):
    qs = super(ArticleList, self).get_queryset()
    # exclude featured articles from queryset, to allow featured article
    # plugin on the list view page without duplicate entries in page qs.
    exclude_count = self.config.exclude_featured
    if exclude_count:
        featured_qs = Article.objects.all().filter(is_featured=True)
        if not self.edit_mode:
            featured_qs = featured_qs.published()
        exclude_featured = featured_qs[:exclude_count].values_list('pk')
        qs = qs.exclude(pk__in=exclude_featured)

    qs = qs.filter(
        translations__language_code=self.request.LANGUAGE_CODE
    )

    return qs


ArticleList.get_queryset = get_queryset


class ArticleRelatedUpdateView(PermissionRequiredMixin, FormView):
    form_class = ArticleForm
    template_name = 'articles/article_update.pug'
    permission_required = ('articles.change_article',)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        # add article object
        self.article = get_object_or_404(Article, pk=kwargs['pk'])

        return super(
            ArticleRelatedUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):

        # send article object to form class
        kwargs = super().get_form_kwargs()
        kwargs.update({'article': self.article})

        return kwargs

    def get_initial(self):
        initial = super(ArticleRelatedUpdateView, self).get_initial()

        # get initial data from article object
        self.initial_list = list(
            self.article.related.translated().values_list('pk', flat=True))

        # Update initial data
        initial.update({
                'related': self.initial_list
            })

        return initial

    def get_context_data(self, **kwargs):
        context = super(ArticleRelatedUpdateView, self).get_context_data(
            **kwargs
        )

        # send article object to template
        context['article'] = self.article

        return context

    def form_valid(self, form):

        # get related id from POST data
        related_id = self.request.POST.getlist('related')

        # remove old related news
        self.article.related.remove(
            *self.initial_list
        )

        # add related news from POST data
        self.article.related.add(*related_id)

        return super(ArticleRelatedUpdateView, self).form_valid(form)

    def get_success_url(self):

        # Go to article detail
        return self.article.get_absolute_url()
