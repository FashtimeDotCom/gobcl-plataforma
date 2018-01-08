from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.pluginmodel import CMSPlugin
from cms.models import Page

from filer.fields.image import FilerImageField


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
