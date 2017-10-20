# -*- coding: utf-8 -*-
""" Models for the presidencies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


class Presidency(BaseModel):
    government_structure = models.OneToOneField(
        'government_structures.GovernmentStructure',
        verbose_name=_('government structure'),
    )
    title = models.CharField(
        _('title'),
        max_length=50,
    )
    description = models.TextField(
        _('description'),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    urls = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('urls'),
    )

    class Meta:
        verbose_name = _('presidency')
        verbose_name_plural = _('presidencies')
        permissions = (
            ('view_presidency', _('Can view presidency')),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns the canonical URL for the Presidency object """

        return reverse('presidency_detail', args=(self.pk,))
