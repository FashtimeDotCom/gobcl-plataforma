# -*- coding: utf-8 -*-
""" Administration classes for the articles application. """
# standard lirary
#
from aldryn_translation_tools.admin import AllTranslationsMixin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from . import models



from cms.admin.placeholderadmin import PlaceholderAdminMixin


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = _(
    "Mark selected articles as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


make_unpublished.short_description = _(
    "Mark selected articles as not published")


def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


make_featured.short_description = _(
    "Mark selected articles as featured")


def make_not_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


make_not_featured.short_description = _(
    "Mark selected articles as not featured")


class ArticleAdminForm(TranslatableModelForm):

    class Meta:
        model = models.Article
        fields = [
            'categories',
            'featured_image',
            'is_featured',
            'is_published',
            'lead_in',
            'meta_description',
            'meta_keywords',
            'meta_title',
            'created_by',
            'slug',
            'tags',
            'title',
        ]

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        qs = models.Article.objects

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)


class ArticleAdmin(
    AllTranslationsMixin,
    PlaceholderAdminMixin,
    FrontendEditableAdminMixin,
    TranslatableAdmin
):
    form = ArticleAdminForm
    list_display = ('title', 'slug', 'is_featured',
                    'is_published', 'created_by')
    list_filter = [
        'categories',
    ]
    actions = (
        make_featured, make_not_featured,
        make_published, make_unpublished,
    )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'publishing_date',
                'is_published',
                'is_featured',
                'featured_image',
                'lead_in',
            )
        }),
        (_('Meta Options'), {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'meta_title',
                'meta_description',
                'meta_keywords',
            )
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'tags',
                'categories',
                'created_by',
            )
        }),
    )
    filter_horizontal = [
        'categories',
    ]

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        request.GET = data

        data['created_by'] = request.user.pk
        request.GET = data
        return super(ArticleAdmin, self).add_view(request, *args, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(is_draft=True)


admin.site.register(models.Article, ArticleAdmin)
