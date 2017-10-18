# -*- coding: utf-8 -*-
""" Models for the public_companies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from institutions.models import Institution


class PublicCompany(Institution):
    public_servants = models.ManyToManyField(
        'public_servants.PublicServant',
        verbose_name=_('public servants'),
        related_name='public_companies'
    )
    public_enterprises = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('public enterprises'),
    )

    class Meta:
        verbose_name = _('public company')
        verbose_name_plural = _('public companies')
        permissions = (
            ('view_publiccompany', _('Can view public company')),
        )

    def __str__(self):
        # TODO this is an example str return, change it
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the PublicCompany object """
        # TODO this is an example, change it
        return reverse('publiccompany_detail', args=(self.pk,))
