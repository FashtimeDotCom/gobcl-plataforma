# -*- coding: utf-8 -*-
""" Administration classes for the campaigns application. """
# standard library

# django
from django.contrib import admin
from aldryn_translation_tools.admin import AllTranslationsMixin

from parler.admin import TranslatableAdmin

# models
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(AllTranslationsMixin, TranslatableAdmin):

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
        'external_url',
        'activation_datetime',
        'deactivation_datetime',
        'is_featured',
        'url',
    )
    readonly_fields = (
    )
    list_filter = (
        'is_featured',
    )

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.title)
    url.allow_tags = True
