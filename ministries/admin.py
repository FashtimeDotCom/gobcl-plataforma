# -*- coding: utf-8 -*-
""" Administration classes for the ministries application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# models
from .models import Ministry, PublicService


@admin.register(Ministry)
class MinistryAdmin(InstitutionAdmin):
    filter_horizontal = (
        'public_servants',
    )


@admin.register(PublicService)
class PublicServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'ministry',
        'url',
    )
