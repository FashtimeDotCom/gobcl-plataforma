# -*- coding: utf-8 -*-
""" Models for the public_servants application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

# models
from base.models import BaseGovernmentStructureModel


class PublicServant(BaseGovernmentStructureModel):
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    charge = models.CharField(
        _('charge'),
        max_length=100,
        null=True,
    )
    description = models.TextField(
        _('description'),
    )
    email = models.EmailField(
        _('email'),
        max_length=50,
    )
    phone = PhoneNumberField(
        _('phone'),
    )
    twitter = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name = _('public servant')
        verbose_name_plural = _('public servants')
        permissions = (
            ('view_public_servant', _('Can view public_servants')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the public_servant object """

        return reverse('public_servant_detail', args=(self.pk,))
