# -*- coding: utf-8 -*-
""" Administration classes for the public_enterprises application. """
# standard library

# django
from django.contrib import admin

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import PublicEnterprise


@admin.register(PublicEnterprise)
class PublicEnterpriseAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'url',
    )
    filter_horizontal = (
        'ministries',
    )
