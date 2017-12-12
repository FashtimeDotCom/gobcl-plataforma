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
    pass


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'service',
        'code',
    )
    list_filter = (
        'service',
    )
    search_fields = (
        'title',
    )
