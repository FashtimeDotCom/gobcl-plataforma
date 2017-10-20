# -*- coding: utf-8 -*-
""" Forms for the presidencies application. """
# standard library

# django
from django import forms

# models
from .models import Presidency

# views
from base.forms import BaseModelForm


class PresidencyForm(BaseModelForm):
    """
    Form Presidency model.
    """

    class Meta:
        model = Presidency
        exclude = ()
