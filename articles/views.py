# -*- coding: utf-8 -*-
""" Views for the articles application. """
# standard library

# django
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

# models
from .models import Article

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
        qs = super(PreviewModeMixin, self).get_queryset()
        # check if user can see unpublished items. this will allow to switch
        # to edit mode instead of 404 on article detail page. CMS handles the
        # permissions.
        user = self.request.user
        user_can_edit = user.is_staff or user.is_superuser

        if self.edit_mode and user_can_edit:
            qs = qs.draft()
        else:
            qs = qs.not_draft()

        if not (self.edit_mode or user_can_edit):
            qs = qs.published()

        language = translation.get_language()
        qs = qs.active_translations(language)
        return qs


class ArticleListView(ListView):
    """
    View for displaying a list of articles.
    """
    model = Article
    template_name = 'articles/article_list.pug'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        queryset = super(ArticleListView, self).get_queryset()
        return queryset.published().translated(is_featured=False)


class ArticleDetailView(PreviewModeMixin, TranslatableSlugMixin,
                        BaseDetailView):
    """
    A view for displaying a single campaign
    """
    model = Article
    template_name = 'articles/article_detail.pug'


def add_text_plugin_to_article(article_id, language='es', content='Doble click para editar el texto',
                               position='last-child'):
    a = Article.objects.get(id=article_id)

    add_plugin(a.content, 'TextPlugin', language, body=content, position=position)


class ArticlePublishView(TranslatableSlugMixin, SingleObjectMixin, BaseRedirectView):
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
        return self.object.get_absolute_url() + '?edit_off'
