# -*- coding: utf-8 -*-
""" Models for the services application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel

from .analytic_client import get_analytic_data


class ChileAtiendeService(BaseModel):
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

    def get_absolute_url(self):
        return self.url or ''


class ChileAtiendeFile(BaseModel):
    service = models.ForeignKey(
        ChileAtiendeService,
        verbose_name=_('service'),
        related_name='files',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
    analytic_visits = models.PositiveIntegerField(
        _('analytic visits'),
        default=0
    )

    class Meta:
        ordering = ('-analytic_visits',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = '{}{}'.format(
                'https://www.chileatiende.gob.cl/fichas/ver/',
                self.code,
            )
        return url

    @classmethod
    def update_visits(cls):
        cls.objects.all().update(analytic_visits=0)

        response = get_analytic_data()

        for report in response.get('reports', []):
            rows = report.get('data', {}).get('rows', [])

            for row in rows:
                dimensions = row.get('dimensions', [])
                values = row.get('metrics', [])

                code = dimensions[0].split('/')[2].split('-')[0]
                visits = values[0]['values'][0]

                cls.objects.filter(
                    code=code
                ).update(
                    analytic_visits=visits
                )
