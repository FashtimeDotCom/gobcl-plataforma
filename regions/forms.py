# -*- coding: utf-8 -*-
""" Forms for the regions application. """
# standard library

# django

# models
from .models import Region

# views
from base.forms import TranslatableModelForm


class RegionForm(TranslatableModelForm):
    """
    Form Region model.
    """

    class Meta:
        model = Region
        exclude = (
            'government_structure',
        )


class RegionCreateForm(RegionForm):
    """
    Form Region model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('government_structure')
