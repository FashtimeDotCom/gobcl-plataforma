# -*- coding: utf-8 -*-
""" Forms for the sociocultural_departments application. """
# standard library

# django
from django import forms

# models
from .models import SocioculturalDepartment

# views
from base.forms import BaseModelForm


class SocioculturalDepartmentForm(BaseModelForm):
    """
    Form SocioculturalDepartment model.
    """

    class Meta:
        model = SocioculturalDepartment
        exclude = ()
