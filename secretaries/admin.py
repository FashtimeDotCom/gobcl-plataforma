# -*- coding: utf-8 -*-
""" Administration classes for the secretaries application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# models
from .models import Secretary


@admin.register(Secretary)
class SecretaryAdmin(InstitutionAdmin):
    pass
