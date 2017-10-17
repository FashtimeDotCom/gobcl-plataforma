# -*- coding: utf-8 -*-
""" Administration classes for the regions application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
