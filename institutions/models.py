# -*- coding: utf-8 -*-
""" Models for the institutions application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# models
from base.models import BaseGovernmentModel, BaseModel


class InstitutionURL(BaseModel):
    url = models.URLField(
        _('url'),
        max_length=200,
    )

    def __str__(self):
        return self.url


class Institution(BaseGovernmentModel):
    # foreign keys
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    description = models.TextField(
        _('description'),
    )
    slug = models.SlugField(
        _('slug'),
        blank=True,
        max_length=255,
        editable=False,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    procedures_and_benefits = models.URLField(
        _('procedures and benefits'),
        max_length=200,
        blank=True,
    )
    authority = models.ForeignKey(
        'public_servants.PublicServant',
        verbose_name=_('authority'),
    )

    class Meta:
        abstract = True

    def clean(self):
        self.name = self.name.strip()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Institution, self).save(**kwargs)
