# -*- coding: utf-8 -*-
""" Administration classes for the public_enterprises application. """
# standard library

# django
from django.contrib import admin

# models
from .models import PublicEnterprise


@admin.register(PublicEnterprise)
class PublicEnterpriseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
    )
    filter_horizontal = (
        'ministries',
    )
