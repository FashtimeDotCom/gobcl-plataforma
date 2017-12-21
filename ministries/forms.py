# -*- coding: utf-8 -*-
""" Forms for the ministries application. """
# standard library

# django

# models
from .models import Ministry
from .models import PublicService

# forms
from base.forms import TranslatableModelForm


class MinistryForm(TranslatableModelForm):
    """
    Form Ministry model.
    """

    class Meta:
        model = Ministry
        exclude = (
            'government_structure',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        public_servants = self.fields['public_servants'].queryset
        public_servants = public_servants.filter(
            government_structure=self.instance.government_structure
        )
        self.fields['public_servants'].queryset = public_servants


class PublicServiceForm(TranslatableModelForm):
    """
    Form PublicService model.
    """

    class Meta:
        model = PublicService
        exclude = ()
