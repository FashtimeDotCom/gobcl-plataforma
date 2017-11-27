# -*- coding: utf-8 -*-
""" Administration classes for the campaigns application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
    )
    list_display = (
        'title',
        'page',
        'is_active',
        'featured_since',
        'featured_until',
    )
    readonly_fields = (
        'page',
    )
    list_filter = (
        'is_active',
    )
