# -*- coding: utf-8 -*-
""" Administration classes for the presidencies application. """
# standard library

# django
from django.contrib import admin

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Presidency, PresidencyURL


@admin.register(Presidency)
class PresidencyAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'title',
        'government_structure',
        'twitter',
        'url',
    )


@admin.register(PresidencyURL)
class PresidencyURLAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = ('url', 'order')
