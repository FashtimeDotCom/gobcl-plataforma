# -*- coding: utf-8 -*-
""" Models for the presidencies application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangocms_text_ckeditor.fields import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField
from parler.models import TranslatableModel
from parler.models import TranslatedFields

# models
from base.models import BaseModel
from base.models import file_path

# elasticsearch
from searches.elasticsearch.documents import SearchIndex

from .managers import PresidencyManager
from .managers import PresidencyURLQueryset

# utils
from base.utils import remove_tags


class PresidencyURL(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=100,
            null=True,
        ),
        description=HTMLField(
            _('description'),
        ),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    order = models.PositiveIntegerField(
        _('order'),
        default=0,
    )

    objects = PresidencyURLQueryset.as_manager()

    def __str__(self):
        return '{} ({})'.format(
            self.name,
            self.url,
        )

    class Meta:
        ordering = ('order',)
        verbose_name = _('presidency url')
        verbose_name_plural = _('presidency urls')
        permissions = (
            ('view_presidency_url', _('Can view presidency urls')),
        )


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
        description=HTMLField(
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

    objects = PresidencyManager()

    class Meta:
        verbose_name = _('presidency')
        verbose_name_plural = _('presidencies')
        permissions = (
            ('view_presidency', _('Can view presidency')),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.index_in_elasticsearch()

        return super(Presidency, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # TODO: unindex
        return super(Presidency, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ Returns the canonical URL for the Presidency object """

        return reverse('presidency_detail')

    def index_in_elasticsearch(self, boost):
        doc = SearchIndex(
            name=self.name,
            title=self.title,
            description=remove_tags(self.description),
            language_code=self.language_code,
            url=self.get_absolute_url(),
            detail=self.title,
            boost=boost
        )
        doc.save()
