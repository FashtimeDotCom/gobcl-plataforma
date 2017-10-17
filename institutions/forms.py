# -*- coding: utf-8 -*-
""" Forms for the institutions application. """
# standard library

# django
from django import forms

# models
from .models import Ministry

# views
from base.forms import BaseModelForm


class MinistryForm(BaseModelForm):
    """
    Form Ministry model.
    """

    class Meta:
        model = Ministry
        exclude = ()
