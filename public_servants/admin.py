# -*- coding: utf-8 -*-
""" Administration classes for the public_servants application. """
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
        'translations__description',
    )

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:public_servants_publicservant_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)
