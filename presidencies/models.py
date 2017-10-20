# -*- coding: utf-8 -*-
""" Models for the presidencies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from easy_thumbnails.fields import ThumbnailerImageField

# models
from base.models import BaseModel
from base.models import file_path

from base.managers import BaseGovernmentQuerySet


class Presidency(BaseModel):
    government_structure = models.OneToOneField(
        'government_structures.GovernmentStructure',
        verbose_name=_('government structure'),
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    title = models.CharField(
        _('title'),
        max_length=50,
    )
    photo = ThumbnailerImageField(
        _('photo'),
        upload_to=file_path,
        null=True,
    )
    description = models.TextField(
        _('description'),
    )
    twitter = models.CharField(
        max_length=50,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    urls = models.ManyToManyField(
        'institutions.InstitutionURL',
        verbose_name=_('urls'),
    )
    slug = models.SlugField(
        _('slug'),
        blank=True,
        max_length=255,
        editable=False,
    )

    objects = BaseGovernmentQuerySet.as_manager()

    class Meta:
        verbose_name = _('presidency')
        verbose_name_plural = _('presidencies')
        permissions = (
            ('view_presidency', _('Can view presidency')),
        )

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(Presidency, self).save(**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns the canonical URL for the Presidency object """

        return reverse('presidency_detail', args=(self.slug,))
