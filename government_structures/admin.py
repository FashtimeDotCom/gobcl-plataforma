# -*- coding: utf-8 -*-
""" Administration classes for the government_structures application. """
# standard library

# django
from django.contrib import admin

# models
from .models import GovernmentStructure


@admin.register(GovernmentStructure)
class GovernmentStructureAdmin(admin.ModelAdmin):
    list_display = (
        'publication_date',
        'current_government',
    )
