# -*- coding: utf-8 -*-
""" Administration classes for the ministries application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from institutions.admin import InstitutionAdmin

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Ministry, PublicService


@admin.register(Ministry)
class MinistryAdmin(InstitutionAdmin):
    list_filter = (
        'government_structure',
    )
    list_display = (
        'name',
        'government_structure',
        'minister',
        'url',
    )

    filter_horizontal = (
        'public_servants',
    )

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:ministries_ministry_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)


@admin.register(PublicService)
class PublicServiceAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'ministry',
        'url',
    )
