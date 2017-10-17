# -*- coding: utf-8 -*-
""" Forms for the secretaries application. """
# standard library

# django
from django import forms

# models
from .models import Secretary

# views
from base.forms import BaseModelForm


class SecretaryForm(BaseModelForm):
    """
    Form Secretary model.
    """

    class Meta:
        model = Secretary
        exclude = ()
