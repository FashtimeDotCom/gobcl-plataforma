# -*- coding: utf-8 -*-
#
""" Models for the cms plugins used in gob.cl"""

# standard library
import os

# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import F

# models
from cms.models.pluginmodel import CMSPlugin
from cms.models import Page
from aldryn_newsblog.models import Article
from base.models import BaseModel
from filer.fields.image import FilerImageField
from filer.fields.image import FilerFileField
from .managers import HeaderImageQueryset


class AudioPlugin(CMSPlugin):
    title = models.CharField(
        _('title'),
        max_length=50,
    )
    audio = FilerFileField(
        verbose_name=_('audio'),
    )
    audio_length = models.CharField(
        _('audio length'),
        max_length=10,
    )

    def __str__(self):
        return os.path.basename(self.audio.path)


class GalleryPlugin(CMSPlugin):
    description = models.TextField(
        _('description'),
        default='',
    )

    def __str__(self):
        return self.description or str(self.id)


class GalleryImagePlugin(CMSPlugin):
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )
    caption = models.TextField(
        _('caption'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.caption or str(self.id)


class HtmlPlugin(CMSPlugin):
    html = models.TextField(
        _('html'),
    )

    def __str__(self):
        return self.html[:50]


class PlainTextPlugin(CMSPlugin):
    text = models.TextField(
        _('text'),
    )

    def __str__(self):
        return self.text[:50]


class HeaderPlugin(CMSPlugin):
    title = models.CharField(
        max_length=60,
        verbose_name=_('title'),
    )
    description = models.TextField(
        _('description'),
        default='',
        blank=True,
    )
    external_link = models.URLField(
        verbose_name=_('External link'),
        blank=True,
        max_length=2040,
        help_text=_('Provide a valid URL to an external website.'),
    )
    internal_link = models.ForeignKey(
        Page,
        verbose_name=_('Internal link'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('If provided, overrides the external link.'),
    )
    link_text = models.CharField(
        max_length=60,
        verbose_name=_('link text'),
        blank=True,
        default=''
    )

    def __str__(self):
        return self.title


class ContentPlugin(CMSPlugin):
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    description = models.TextField(
        _('description'),
    )
    last_elements_on_right_column = models.PositiveIntegerField(
        _('move last x elements to right '),
        default=0,
        help_text=_(
            'move the number of last elements indicated by this field to the'
            ' right column'
        )
    )
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class ArticleCount(BaseModel):
    article = models.OneToOneField(
        Article,
        verbose_name=_('article'),
        related_name='count',
        null=True,
    )
    visits = models.PositiveIntegerField(
        _('visits'),
        default=0
    )

    class Meta:
        ordering = ('visits',)

    def __str__(self):
        return self.article.title

    def increase(self):
        self.visits = F('visits') + 1
        self.save()

    def decrease(self):
        self.visits = F('visits') - 1
        self.save()


class HeaderImage(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=150,
    )
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )

    objects = HeaderImageQueryset.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            HeaderImage.objects.filter(
                is_active=True
            ).update(is_active=False)
        return super(HeaderImage, self).save(*args, **kwargs)
