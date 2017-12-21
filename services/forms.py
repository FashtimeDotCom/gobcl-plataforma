# -*- coding: utf-8 -*-
""" Forms for the services application. """
# standard library

# django
from django import forms

# models
from .models import Service

# views
from base.forms import BaseModelForm


class ServiceForm(BaseModelForm):
    """
    Form Service model.
    """

    class Meta:
        model = Service
        exclude = ()
