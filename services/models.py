# -*- coding: utf-8 -*-
""" Models for the services application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


class Service(BaseModel):
    code = models.CharField(
        _('code'),
        max_length=255,
        unique=True,
    )
    initial = models.CharField(
        _('initial'),
        max_length=255,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )
    mision = models.TextField(
        _('mision'),
    )

    def __str__(self):
        return self.name


class File(BaseModel):
    service = models.ForeignKey(
        Service,
        verbose_name=_('service'),
        related_name='files',
        null=True,
        blank=True,
    )
    service_name = models.CharField(
        _('service name'),
        max_length=255,
    )
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    code = models.CharField(
        _('code'),
        max_length=255,
        unique=True,
    )
    date = models.DateTimeField(
        _('date'),
        blank=True,
        null=True,
    )
    objective = models.TextField(
        _('objective'),
    )
    beneficiaries = models.TextField(
        _('beneficiaries'),
    )
    cost = models.TextField(
        _('cost'),
    )
    period = models.TextField(
        _('period'),
    )
    duration = models.TextField(
        _('duration'),
    )

    def __str__(self):
        return self.title
