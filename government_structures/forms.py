# -*- coding: utf-8 -*-
""" Forms for the government_structures application. """
# standard library

# django
from django import forms

# models
from .models import GovernmentStructure

# views
from base.forms import BaseModelForm


class GovernmentStructureForm(BaseModelForm):
    """
    Form GovernmentStructure model.
    """

    class Meta:
        model = GovernmentStructure
        exclude = ()
