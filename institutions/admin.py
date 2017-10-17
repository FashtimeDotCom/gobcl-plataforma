# -*- coding: utf-8 -*-
""" Administration classes for the institutions application. """
# standard library

# django
from django.contrib import admin

from .models import InstitutionURL


class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'government',
        'url',
    )
    search_fields = (
        'name',
        'url',
        'description',
    )
    list_filter = (
        'government__current_government',
    )


@admin.register(InstitutionURL)
class InstitutionURLAdmin(admin.ModelAdmin):
    pass
