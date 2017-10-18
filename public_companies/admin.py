# -*- coding: utf-8 -*-
""" Administration classes for the public_companies application. """
# standard library

# django
from django.contrib import admin

from institutions.admin import InstitutionAdmin

# models
from .models import PublicCompany


@admin.register(PublicCompany)
class PublicCompanyAdmin(InstitutionAdmin):
    pass
