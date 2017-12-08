# -*- coding: utf-8 -*-
""" Forms for the campaigns application. """
# standard library

# django

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
            'activation_datetime',
            'deactivation_datetime',
            'is_featured',
        )
