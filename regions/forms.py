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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        public_servants = self.fields['governor'].queryset
        public_servants = public_servants.filter(
            government_structure=self.instance.government_structure
        )
        self.fields['governor'].queryset = public_servants
