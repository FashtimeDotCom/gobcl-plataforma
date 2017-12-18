# -*- coding: utf-8 -*-
""" Administration classes for the contingencies application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Contingency


@admin.register(Contingency)
class ContingencyAdmin(admin.ModelAdmin):
    pass
