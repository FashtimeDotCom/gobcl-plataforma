# -*- coding: utf-8 -*-
""" Administration classes for the campaigns application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass
