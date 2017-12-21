# -*- coding: utf-8 -*-
""" Forms for the ministries application. """
# standard library

# django

# models
from .models import Ministry
from .models import PublicService

# views
from base.forms import BaseModelForm
from parler.forms import TranslatableModelForm


class MinistryForm(TranslatableModelForm):
    """
    Form Ministry model.
    """

    class Meta:
        model = Ministry
        exclude = ()


class PublicServiceForm(BaseModelForm):
    """
    Form PublicService model.
    """

    class Meta:
        model = PublicService
        exclude = ()
