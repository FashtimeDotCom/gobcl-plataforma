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
    minister = models.ForeignKey(
        'public_servants.PublicServant',
        verbose_name=_('minister'),
        null=True,
    )
    public_servants = models.ManyToManyField(
        'public_servants.PublicServant',
        verbose_name=_('public servants'),
        related_name='ministries'
    )
    public_enterprises = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('public enterprises'),
    )
    procedures_and_benefits = models.URLField(
        _('procedures and benefits'),
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = _('ministry')
        verbose_name_plural = _('ministries')
        unique_together = ('name', 'government_structure')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the public_servant object """
        return reverse('ministry_detail', args=(self.slug,))
