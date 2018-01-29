# -*- coding: utf-8 -*-
""" Forms for the streams application. """
# standard library

# django
from django import forms

# models
from .models import Stream

# views
from base.forms import BaseModelForm


class StreamForm(BaseModelForm):
    """
    Form Stream model.
    """

    class Meta:
        model = Stream
        exclude = ()
