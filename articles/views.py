# -*- coding: utf-8 -*-
""" Views for the articles application. """
# standard library
import json

# django
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

# models
from .models import Article
from aldryn_categories.models import Category

# views
from base.views import BaseDetailView
from base.views import BaseRedirectView
from parler.views import TranslatableSlugMixin


from cms.api import add_plugin


class EditModeMixin(object):
    """
    A mixin which sets the property 'edit_mode' with the truth value for
    whether a user is logged-into the CMS and is in edit-mode.
    """
    edit_mode = False

    def dispatch(self, request, *args, **kwargs):
        self.edit_mode = (
            self.request.toolbar and self.request.toolbar.edit_mode)
        return super(EditModeMixin, self).dispatch(request, *args, **kwargs)


class PreviewModeMixin(EditModeMixin):
    """
    If content editor is logged-in, show all articles. Otherwise, only the
    published articles should be returned.
    """

    def get_queryset(self):
        qs = super(PreviewModeMixin, self).get_queryset().translated()
        # check if user can see unpublished items. this will allow to switch
        # to edit mode instead of 404 on article detail page. CMS handles the
        # permissions.
        user = self.request.user
        user_can_edit = user.is_staff or user.is_superuser

        if not user_can_edit:
            qs = qs.published()
        else:
            # user can edit
            if self.edit_mode:
                qs = qs.draft()
            else:
                published_exists = True

                if hasattr(self, 'slug_url_kwarg'):
                    slug = self.kwargs.get(self.slug_url_kwarg)
                    if not qs.published().translated(slug=slug).exists():
                        published_exists = False
                        qs = qs.draft()

                if published_exists:
                    qs = qs.published()

        language = translation.get_language()
        qs = qs.active_translations(language)
        return qs


class ArticleListView(PreviewModeMixin, ListView):
    """
    View for displaying a list of articles.
    """
    model = Article
    template_name = 'articles/article_list.pug'
    paginate_by = 8
    page_kwarg = 'p'

    def get_pagination_options(self):
        # Django does not handle negative numbers well
        # when using variables.
        # So we perform the conversion here.
        options = {
            'pages_start': 10,
            'pages_visible': 4,
        }

        pages_visible_negative = -options['pages_visible']
        options['pages_visible_negative'] = pages_visible_negative
        options['pages_visible_total'] = options['pages_visible'] + 1
        options['pages_visible_total_negative'] = pages_visible_negative - 1
        return options

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['pagination'] = self.get_pagination_options()

        featured_qs = Article.objects.all().translated(is_featured=True)

        context['featured_article'] = featured_qs.first()

        return context

    def get_queryset(self):
        qs = super(ArticleListView, self).get_queryset()

        featured_qs = Article.objects.all().translated(is_featured=True)

        if not self.edit_mode:
            featured_qs = featured_qs.published()

        # exclude 1 featured article
        exclude_featured = featured_qs[:1].values_list('pk')
        qs = qs.exclude(pk__in=exclude_featured)

        return qs


class ArticleDetailView(PreviewModeMixin, TranslatableSlugMixin,
                        BaseDetailView):
    """
    A view for displaying a single campaign
    """
    model = Article
    template_name = 'articles/article_detail.pug'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['edit_mode'] = json.dumps(self.edit_mode)
        return context


def add_text_plugin_to_article(
    article_id,
    language='es',
    content='Doble click para editar el texto',
    position='last-child'
):
    a = Article.objects.get(id=article_id)

    add_plugin(a.content, 'TextPlugin', language,
               body=content, position=position)


class ArticlePublishView(
    TranslatableSlugMixin,
    SingleObjectMixin,
    BaseRedirectView
):
    permanent = False
    permission_required = 'articles.change_article'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Article.objects.draft()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        language = translation.get_language()
        self.object.publish(language)

        return super(ArticlePublishView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        url = self.object.get_absolute_url()

        # remove ?edit string from url
        return url.replace('?edit', '') + '?edit_off'


class ArticleUnpublishView(
    TranslatableSlugMixin,
    SingleObjectMixin,
    BaseRedirectView
):
    permanent = False
    permission_required = 'articles.change_article'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Article.objects.published()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        language = translation.get_language()
        self.object.unpublish(language)

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        url = self.object.get_absolute_url()

        # remove ?edit_off string from url
        return url.replace('?edit_off', '') + '?edit'


class CategoryArticleList(ArticleListView):
    """A list of articles filtered by categories."""
    def get_queryset(self):
        return super(CategoryArticleList, self).get_queryset().filter(
            categories=self.category
        )

    def get(self, request, category):
        self.category = get_object_or_404(
            Category, translations__slug=category)
        return super(CategoryArticleList, self).get(request)

    def get_context_data(self, **kwargs):
        kwargs['newsblog_category'] = self.category
        ctx = super(CategoryArticleList, self).get_context_data(**kwargs)
        ctx['newsblog_category'] = self.category
        return ctx
