# -*- coding: utf-8 -*-
""" Administration classes for the services application. """
# standard library

# django
from django.contrib import admin

# models
from .models import ChileAtiendeService
from .models import ChileAtiendeFile


@admin.register(ChileAtiendeService)
class ChileAtiendeServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'initial',
        'code',
    )
    search_fields = (
        'name',
    )


@admin.register(ChileAtiendeFile)
class ChileAtiendeFileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'service',
        'code',
        'analytic_visits',
    )
    list_filter = (
        'service',
    )
    search_fields = (
        'title',
    )
