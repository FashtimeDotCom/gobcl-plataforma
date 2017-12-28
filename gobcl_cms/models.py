from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField


class GalleryPlugin(CMSPlugin):
    description = models.CharField(
        _('description'),
        max_length=255,
        default='',
        blank=True,
    )

    def __str__(self):
        return self.description or str(self.id)


class GalleryImagePlugin(CMSPlugin):
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )
    caption = models.CharField(
        _('caption'),
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.caption or str(self.id)


class HtmlPlugin(CMSPlugin):
    html = models.TextField(
        _('html'),
    )
