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
            'image',
        )

    class Media:
        extend = False
        css = {
            'all': [
                'filer/css/admin_filer.css',
            ]
        }
        js = (
            'admin/js/core.js',
            'admin/js/jquery.js',
            'admin/js/jquery.init.js',
            'admin/js/admin/RelatedObjectLookups.js',
            'admin/js/actions.js',
            'admin/js/urlify.js',
            'admin/js/prepopulate.js',
            'filer/js/libs/dropzone.min.js',
            'filer/js/addons/dropzone.init.js',
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
            'admin/js/related-widget-wrapper.js',
        )
