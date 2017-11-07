# -*- coding: utf-8 -*-
""" Models for the public_enterprises application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseGovernmentStructureModel


class PublicEnterprise(BaseGovernmentStructureModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        null=True,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )
    ministries = models.ManyToManyField(
        'ministries.Ministry',
        verbose_name=_('ministries'),
        blank=True,
    )

    class Meta:
        verbose_name = _('public enterprise')
        verbose_name_plural = _('public enterprises')
        permissions = (
            ('view_publicenterprise', _('Can view public enterprise')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the PublicEnterprise object """
        return reverse('public_enterprise_detail', args=(self.pk,))
