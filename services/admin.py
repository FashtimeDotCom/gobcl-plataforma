# -*- coding: utf-8 -*-
""" Administration classes for the services application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Service
from .models import File


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'initial',
        'code',
    )
    search_fields = (
        'name',
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
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
