from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from filer.fields.image import FilerImageField


class ImagePLugin(CMSPlugin):
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
    )
