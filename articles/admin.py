# -*- coding: utf-8 -*-
""" Administration classes for the articles application. """
# standard lirary

# django
from django.contrib import admin

from parler.admin import TranslatableAdmin

# models
from .models import Article


@admin.register(Article)
class ArticleAdmin(TranslatableAdmin):
    def get_prepopulated_fields(self, request, obj=None):
        # can't use `prepopulated_fields = ..` because it breaks the admin
        # validation for translated fields. This is the official django-parler
        # workaround.
        return {
            'slug': ('title',)
        }

    search_fields = (
        'translations__title',
        'translations__description',
    )
    list_display = (
        'title',
        'publishing_date',
        'is_featured',
        'url',
    )
    readonly_fields = (
    )
    list_filter = (
        'publishing_date',
    )

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.title)
    url.allow_tags = True
