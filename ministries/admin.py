# -*- coding: utf-8 -*-
""" Administration classes for the ministries application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Ministry, PublicService


@admin.register(Ministry)
class MinistryAdmin(InstitutionAdmin):
    list_display = (
        'name',
        'government_structure',
        'minister',
        'url',
    )

    filter_horizontal = (
        'public_servants',
    )


@admin.register(PublicService)
class PublicServiceAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'ministry',
        'url',
    )
