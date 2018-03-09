# -*- coding: utf-8 -*-
""" Administration classes for the regions application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from institutions.admin import InstitutionAdmin

# models
from .models import Region, Commune


@admin.register(Region)
class RegionAdmin(InstitutionAdmin):
    list_filter = ('government_structure',)
    list_display = (
        'name',
        'government_structure',
        'governor',
        'url',
    )

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:regions_region_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    list_display = (
        'name',
        'region',
        'email',
        'phone',
        'twitter',
        'url',
    )
