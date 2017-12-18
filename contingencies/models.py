# -*- coding: utf-8 -*-
""" Models for the contingencies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


def default_end_datetime():
    return timezone.now() + timezone.timedelta(7)


class Contingency(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=255,
        blank=True,
    )
    lead = models.TextField(
        _('lead'),
        blank=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    activation_datetime = models.DateTimeField(
        _('activation datetime`'),
        default=timezone.now,
        help_text=_('The date this contingency will be activated'),
    )
    deactivation_datetime = models.DateTimeField(
        _('deactivation datetime`'),
        default=default_end_datetime,
        help_text=_('The date this contingency will be deactivated'),
    )

    class Meta:
        verbose_name = _('contingency')
        verbose_name_plural = _('contingencies')
        permissions = (
            ('view_contingency', _('Can view contingency')),
        )

    def __str__(self):
        # TODO this is an example str return, change it
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the Contingency object """
        # TODO this is an example, change it
        return reverse('contingency_detail', args=(self.pk,))


class ContingencyValue(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
    )
    date_time = models.DateTimeField(
        _(''),
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url
