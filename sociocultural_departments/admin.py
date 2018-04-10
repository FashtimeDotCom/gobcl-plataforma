# -*- coding: utf-8 -*-
""" Administration classes for the sociocultural_departments application. """
# standard library

# django
from django.contrib import admin

# models
from .models import SocioculturalDepartment
from .models import SocioculturalDepartmentURL

from institutions.admin import GovernmentStructureFilter

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin


@admin.register(SocioculturalDepartment)
class SocioculturalDepartmentAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_filter = (
        ('government_structure', GovernmentStructureFilter),
    )
    list_display = (
        'name',
        'title',
        'government_structure',
        'twitter',
        'url',
    )
    filter_horizontal = (
        'urls',
    )


@admin.register(SocioculturalDepartmentURL)
class SocioculturalDepartmentURLAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'url',
        'name',
        'order',
    )
