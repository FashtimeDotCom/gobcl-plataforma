# -*- coding: utf-8 -*-
""" Administration classes for the ministries application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# models
from .models import Ministry


@admin.register(Ministry)
class MinistryAdmin(InstitutionAdmin):
    filter_horizontal = (
        'public_servants',
        'public_enterprises',
    )
