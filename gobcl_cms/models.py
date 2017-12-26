from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField


class ImagePlugin(CMSPlugin):
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


class HtmlPlugin(CMSPlugin):
    html = models.TextField(
        _('html'),
    )
