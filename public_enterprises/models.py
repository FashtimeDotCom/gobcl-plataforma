# -*- coding: utf-8 -*-
""" Models for the public_enterprises application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseGovernmentStructureModel

# elasticsearch
from searches.elasticsearch.documents import SearchIndex

from parler.models import TranslatableModel
from parler.models import TranslatedFields

from .managers import PublicEnterpriseManager


class PublicEnterprise(TranslatableModel, BaseGovernmentStructureModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=100,
            null=True,
        )
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )
    ministries = models.ManyToManyField(
        'ministries.Ministry',
        verbose_name=_('ministries'),
        blank=True,
    )

    objects = PublicEnterpriseManager()

    class Meta:
        verbose_name = _('public enterprise')
        verbose_name_plural = _('public enterprises')
        permissions = (
            ('view_publicenterprise', _('Can view public enterprise')),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return_value = super(PublicEnterprise, self).save(*args, **kwargs)

        self.reindex_in_elasticsearch()

        return return_value

    def get_absolute_url(self):
        """ Returns the canonical URL for the PublicEnterprise object """
        return self.url

    def index_in_elasticsearch(self, boost):
        doc = SearchIndex(
            name=self.name,
            language_code=self.language_code,
            url=self.get_absolute_url(),
            detail=self.url,
            boost=boost
        )
        doc.save(obj=self)
