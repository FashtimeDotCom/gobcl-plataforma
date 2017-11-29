# -*- coding: utf-8 -*-
""" Forms for the campaigns application. """
# standard library

# django
from django import forms

# models
from .models import Campaign

# views
from base.forms import BaseModelForm


class CampaignForm(BaseModelForm):
    """
    Form Campaign model.
    """

    class Meta:
        model = Campaign
        exclude = ()
