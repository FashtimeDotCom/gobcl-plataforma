from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool

from .models import ImagePLugin


class GalleryCMSPLugin(CMSPluginBase):
    model = CMSPlugin
    cache = False
    name = _('Gallery')
    render_template = "cms_plugins/gallery.pug"
    child_classes = ('ImageCMSPlugin',)
    allow_children = True


class ImageCMSPlugin(CMSPluginBase):
    name = _('Image')
    model = ImagePLugin
    render_plugin = False


plugin_pool.register_plugin(GalleryCMSPLugin)
plugin_pool.register_plugin(ImageCMSPlugin)
