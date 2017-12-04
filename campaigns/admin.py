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
    search_fields = (
        'title',
    )
    list_display = (
        'title',
        'page',
        'is_active',
        'is_featured',
        'url',
    )
    readonly_fields = (
        'page',
    )
    list_filter = (
        'is_active',
    )

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.title)
    url.allow_tags = True
