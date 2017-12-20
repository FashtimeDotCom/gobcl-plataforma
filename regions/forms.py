# -*- coding: utf-8 -*-
""" Forms for the regions application. """
# standard library

# django

# models
from .models import Region

# views
from parler.forms import TranslatableModelForm


class RegionForm(TranslatableModelForm):
    """
    Form Region model.
    """

    class Meta:
        model = Region
        exclude = ()
