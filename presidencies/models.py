# -*- coding: utf-8 -*-
""" Models for the presidencies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField
from parler.models import TranslatableModel
from parler.models import TranslatedFields

# models
from base.models import BaseModel
from base.models import file_path


class PresidencyURL(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=100,
            null=True,
        ),
        description=models.TextField(
            _('description'),
        ),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )

    def __str__(self):
        return self.url


class Presidency(BaseModel, TranslatableModel):
    government_structure = models.OneToOneField(
        'government_structures.GovernmentStructure',
        verbose_name=_('government structure'),
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=50,
        ),
        description=models.TextField(
            _('description'),
        ),
    )
    photo = ThumbnailerImageField(
        _('photo'),
        upload_to=file_path,
        null=True,
    )
    twitter = models.CharField(
        max_length=50,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    urls = models.ManyToManyField(
        'PresidencyURL',
        verbose_name=_('urls'),
    )

    class Meta:
        verbose_name = _('presidency')
        verbose_name_plural = _('presidencies')
        permissions = (
            ('view_presidency', _('Can view presidency')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the canonical URL for the Presidency object """

        return reverse('presidency_detail', args=(self.slug,))
