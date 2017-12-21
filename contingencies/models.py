# -*- coding: utf-8 -*-
""" Models for the contingencies application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from parler.models import TranslatableModel
from parler.models import TranslatedFields

# models
from base.models import BaseModel

from .managers import ContingencyQueryset
from .managers import ContingencyEventQueryset


class Contingency(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=255,
        ),
        lead=models.TextField(
            _('lead'),
            blank=True,
        ),
        description=models.TextField(
            _('description'),
            blank=True,
        )
    )
    is_active = models.BooleanField(
        _('is active'),
        default=False,
    )

    objects = ContingencyQueryset.as_manager()

    class Meta:
        verbose_name = _('contingency')
        verbose_name_plural = _('contingencies')
        permissions = (
            ('view_contingency', _('Can view contingency')),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Contingency, self).save(*args, **kwargs)


class ContingencyEvent(BaseModel, TranslatableModel):
    contingency = models.ForeignKey(
        Contingency,
        verbose_name=_('contingency'),
        related_name='events',
    )
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=255,
        ),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )
    date_time = models.DateTimeField(
        _('date time'),
        default=timezone.now,
    )

    objects = ContingencyEventQueryset.as_manager()

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class ContingencyInformation(BaseModel, TranslatableModel):
    contingency = models.ForeignKey(
        Contingency,
        verbose_name=_('contingency'),
        related_name='informations',
    )
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=255,
        ),
        description=models.TextField(
            _('description'),
        )
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        null=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url
