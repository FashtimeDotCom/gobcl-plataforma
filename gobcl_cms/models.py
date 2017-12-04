from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.pluginmodel import CMSPlugin
from base.models import BaseModel

from filer.fields.image import FilerImageField


class GalleryPLugin(CMSPlugin):

    def __str__(self):
        return str(self.id)


class ImageGallery(BaseModel):
    gallery = models.ForeignKey(
        GalleryPLugin,
        null=True,
    )
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )
    order = models.PositiveSmallIntegerField(
        _('order'),
        default=0,
    )

    class Meta:
        ordering = (
            'order',
        )


class HtmlPlugin(CMSPlugin):
    html = models.TextField(
        _('html'),
    )
