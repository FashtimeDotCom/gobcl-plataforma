# -*- coding: utf-8 -*-
""" Administration classes for the presidencies application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Presidency, PresidencyURL


@admin.register(Presidency)
class PresidencyAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_filter = ('government_structure',)
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

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:presidencies_presidency_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)


@admin.register(PresidencyURL)
class PresidencyURLAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = ('url', 'name', 'order')
