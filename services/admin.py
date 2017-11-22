# -*- coding: utf-8 -*-
""" Administration classes for the services application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
