# -*- coding: utf-8 -*-
""" Models for the governments application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


class Government(BaseModel):
    publication_date = models.DateField(
        _('publication date'),
    )
    current_government = models.BooleanField(
        _('current government'),
        default=False,
    )

    class Meta:
        verbose_name = _('government')
        verbose_name_plural = _('governments')
        permissions = (
            ('view_government', _('Can view governments')),
        )

    def __str__(self):
        return '{}'.format(self.publication_date)

    def save(self, **kwargs):
        # Make sure the default government are unique
        if self.current_government:
            Government.objects.filter(
                current_government=True,
            ).update(
                current_government=False,
            )
        super(Government, self).save(**kwargs)
