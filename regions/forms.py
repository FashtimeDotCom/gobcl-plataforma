# -*- coding: utf-8 -*-
""" Forms for the regions application. """
# standard library

# django
from django import forms

# models
from .models import Region

# views
from base.forms import BaseModelForm


class RegionForm(BaseModelForm):
    """
    Form Region model.
    """

    class Meta:
        model = Region
        exclude = ()
