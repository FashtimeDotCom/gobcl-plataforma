# -*- coding: utf-8 -*-
""" Administration classes for the links application. """
# standard library

# django
from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

# models
from .models import FooterLink


@admin.register(FooterLink)
class FooterLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'url',
    )
    ordering = (
        'order',
    )
