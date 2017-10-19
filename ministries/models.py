# -*- coding: utf-8 -*-
""" Models for the ministries application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from institutions.models import Institution


class Ministry(Institution):
    public_servants = models.ManyToManyField(
        'public_servants.PublicServant',
        verbose_name=_('public servants'),
        related_name='ministries'
    )
    public_enterprises = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('public enterprises'),
    )

    class Meta:
        verbose_name = _('ministry')
        verbose_name_plural = _('ministries')
        unique_together = ('name', 'government_structure')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the public_servant object """
        # TODO this is an example, change it
        return reverse('ministry_detail', args=(self.slug,))
