# -*- coding: utf-8 -*-
""" Administration classes for the presidencies application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Presidency, PresidencyURL


@admin.register(Presidency)
class PresidencyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'title',
        'government_structure',
        'twitter',
        'url',
    )


@admin.register(PresidencyURL)
class PresidencyURLAdmin(admin.ModelAdmin):
    list_display = ('url',)
