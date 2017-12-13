# -*- coding: utf-8 -*-
""" Models for the institutions application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# models
from base.models import BaseGovernmentStructureModel

# hitcount
from hitcount.models import HitCountMixin

# parler
from parler.models import TranslatableModel
from parler.models import TranslatedFields

#
from institutions.managers import InstitutionQuerySet


institution_translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=255,
        ),
        description=models.TextField(
            _('description'),
        ),
        slug=models.SlugField(
            _('slug'),
            blank=True,
            max_length=255,
            editable=False,
        ),
    )


class Institution(
        TranslatableModel, BaseGovernmentStructureModel, HitCountMixin):

    url = models.URLField(
        _('url'),
        max_length=200,
    )

    objects = InstitutionQuerySet.as_manager()

    class Meta:
        abstract = True

    def clean(self):
        self.name = self.name.strip()
        self.slug = slugify(self.name)

    def save(self, **kwargs):
        super(Institution, self).save(**kwargs)
