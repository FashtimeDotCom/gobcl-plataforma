# -*- coding: utf-8 -*-
""" Administration classes for the regions application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# models
from .models import Region, Commune


@admin.register(Region)
class RegionAdmin(InstitutionAdmin):
    pass


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'region',
        'email',
        'phone',
        'twitter',
        'url',
    )
