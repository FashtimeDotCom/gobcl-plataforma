# -*- coding: utf-8 -*-
""" Administration classes for the sociocultural_departments application. """
# standard library

# django
from django.contrib import admin

# models
from .models import SocioculturalDepartment
from .models import SocioculturalDepartmentURL


@admin.register(SocioculturalDepartment)
class SocioculturalDepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(SocioculturalDepartmentURL)
class SocioculturalDepartmentURLAdmin(admin.ModelAdmin):
    pass
