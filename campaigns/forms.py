# -*- coding: utf-8 -*-
""" Forms for the campaigns application. """
# standard library

# django
from django import forms

# models
from .models import Campaign

# parler
from parler.forms import TranslatableModelForm


class CampaignForm(TranslatableModelForm):
    """
    Form Campaign model.
    """

    class Meta:
        model = Campaign
        fields = (
            'title',
            'description',
            'external_url',
            'is_active',
            'is_featured',
        )
