# -*- coding: utf-8 -*-
""" Administration classes for the governments application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Government


@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    list_display = (
        'publication_date',
        'current_government',
    )
