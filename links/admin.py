# -*- coding: utf-8 -*-
""" Administration classes for the links application. """
# standard library

# django
from django.contrib import admin

# models
from .models import FooterLink


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
    )
