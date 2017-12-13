# -*- coding: utf-8 -*-
""" Administration classes for the institutions application. """
# standard library

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin


class InstitutionAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'government_structure',
        'url',
    )
    search_fields = (
        'name',
        'url',
        'description',
    )
    list_filter = (
        'government_structure__current_government',
    )
