# -*- coding: utf-8 -*-
""" Forms for the public_servants application. """
# standard library

# django
from django import forms

# models
from .models import PublicServant

# views
from base.forms import BaseModelForm


class PublicServantForm(BaseModelForm):
    """
    Form PublicServant model.
    """

    class Meta:
        model = PublicServant
        exclude = ()
