# -*- coding: utf-8 -*-
""" Models for the institutions application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# models
from base.models import BaseGovernmentStructureModel, BaseModel


class InstitutionURL(BaseModel):
    url = models.URLField(
        _('url'),
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.url


class Institution(BaseGovernmentStructureModel):
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

    class Meta:
        abstract = True

    def clean(self):
        self.name = self.name.strip()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Institution, self).save(**kwargs)
