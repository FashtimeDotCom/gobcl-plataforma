# -*- coding: utf-8 -*-
""" Forms for the public_enterprises application. """
# standard library

# django
from django import forms

# models
from .models import PublicEnterprise

# views
from base.forms import BaseModelForm


class PublicEnterpriseForm(BaseModelForm):
    """
    Form PublicEnterprise model.
    """

    class Meta:
        model = PublicEnterprise
        exclude = ()
