# -*- coding: utf-8 -*-
""" Models for the secretaries application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from institutions.models import Institution


class Secretary(Institution):
    public_servants = models.ManyToManyField(
        'public_servants.PublicServant',
        verbose_name=_('public servants'),
        related_name='secretaries',
    )
    public_enterprises = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('public enterprises'),
    )

    class Meta:
        unique_together = ('name', 'government_structure')
        verbose_name = _('secretary')
        verbose_name_plural = _('secretaries')
        permissions = (
            ('view_secretary', _('Can view secretary')),
        )

    def __str__(self):
        # TODO this is an example str return, change it
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the Secretary object """
        # TODO this is an example, change it
        return reverse('secretary_detail', args=(self.slug,))
