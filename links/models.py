# -*- coding: utf-8 -*-
""" Models for the links application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseGovernmentStructureModel


class FooterLink(BaseGovernmentStructureModel):
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )

    class Meta:
        verbose_name = _('footer link')
        verbose_name_plural = _('footer links')
        permissions = (
            ('view_link', _('Can view link')),
        )

    def __str__(self):
        return self.name
