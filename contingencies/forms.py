# -*- coding: utf-8 -*-
""" Forms for the contingencies application. """
# standard library

# django
from django import forms

# models
from .models import Contingency

# views
from base.forms import BaseModelForm


class ContingencyForm(BaseModelForm):
    """
    Form Contingency model.
    """

    class Meta:
        model = Contingency
        exclude = ()
