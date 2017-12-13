# -*- coding: utf-8 -*-
""" Administration classes for the public_servants application. """
# standard library

# django
from django.contrib import admin

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import PublicServant


@admin.register(PublicServant)
class PublicServantAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_filter = ('government_structure',)
    list_display = (
        'name',
        'government_structure',
        'email',
        'phone',
        'twitter',
    )
    search_fields = (
        'name',
        'email',
        'phone',
        'twitter',
        'description',
    )
