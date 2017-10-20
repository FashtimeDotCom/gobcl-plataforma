# -*- coding: utf-8 -*-
""" Administration classes for the presidencies application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Presidency


@admin.register(Presidency)
class PresidencyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'government_structure',
    )
