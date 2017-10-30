# -*- coding: utf-8 -*-
""" Forms for the links application. """
# standard library

# django
from django import forms

# models
from .models import Link

# views
from base.forms import BaseModelForm


class LinkForm(BaseModelForm):
    """
    Form Link model.
    """

    class Meta:
        model = Link
        exclude = ()
