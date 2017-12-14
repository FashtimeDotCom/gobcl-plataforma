# -*- coding: utf-8 -*-
""" Models for the regions application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

# models
from base.models import BaseModel
from institutions.models import Institution

from institutions.models import institution_translations

# managers
from .managers import CommuneQuerySet


class Region(Institution):
    translations = institution_translations

    # foreign keys
    governor = models.ForeignKey(
        'public_servants.PublicServant',
        verbose_name=_('governor'),
        null=True,
        on_delete=models.SET_NULL,
    )

    # required fields
    email = models.EmailField(
        _('email'),
        max_length=100,
        null=True,
    )
    phone = PhoneNumberField(
        _('phone'),
        null=True,
    )
    twitter = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(
        _('order'),
        default=0,
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        permissions = (
            ('view_region', _('Can view regions')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the region object """

        return reverse('region_detail', args=(self.slug,))


class Commune(BaseModel):
    # foreign keys
    region = models.ForeignKey(
        'Region',
        verbose_name=_('region'),
    )
    # required fields
    name = models.CharField(
        _('name'),
        max_length=50,
    )
    description = models.TextField(
        _('description'),
    )
    email = models.EmailField(
        _('email'),
        max_length=100,
    )
    phone = PhoneNumberField(
        _('phone'),
    )
    twitter = models.CharField(
        max_length=50,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    has_own_municipality = models.BooleanField(
        default=True,
    )
    municipality_latitude = models.FloatField(
        _('latitude'),
        blank=True,
        null=True,
    )
    municipality_longitude = models.FloatField(
        _('longitude'),
        blank=True,
        null=True,
    )

    objects = CommuneQuerySet.as_manager()

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('commune')
        verbose_name_plural = _('communes')
        permissions = (
            ('view_commune', _('Can view communes')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the region object """

        return reverse('region_detail', args=(self.region_pk,))
