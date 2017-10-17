# -*- coding: utf-8 -*-
""" Forms for the governments application. """
# standard library

# django
from django import forms

# models
from .models import Government

# views
from base.forms import BaseModelForm


class GovernmentForm(BaseModelForm):
    """
    Form Government model.
    """

    class Meta:
        model = Government
        exclude = ()
