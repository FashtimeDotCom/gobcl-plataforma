# -*- coding: utf-8 -*-
""" Administration classes for the secretaries application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Secretarie


@admin.register(Secretarie)
class SecretarieAdmin(admin.ModelAdmin):
    pass
