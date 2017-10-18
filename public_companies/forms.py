# -*- coding: utf-8 -*-
""" Forms for the public_companies application. """
# standard library

# django
from django import forms

# models
from .models import PublicCompany

# views
from base.forms import BaseModelForm


class PublicCompanyForm(BaseModelForm):
    """
    Form PublicCompany model.
    """

    class Meta:
        model = PublicCompany
        exclude = ()
