from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GalleryImagePlugin
from .models import HtmlPlugin
from .models import GalleryPlugin
from .models import ContentPlugin


class GalleryCMSPlugin(CMSPluginBase):
    model = GalleryPlugin
    cache = False
    name = _('Gallery')
    render_template = 'cms_plugins/gallery/gallery.pug'
    child_classes = ('ImageCMSPlugin',)
    allow_children = True


class ImageCMSPlugin(CMSPluginBase):
    name = _('Image')
    model = GalleryImagePlugin
    render_template = 'cms_plugins/gallery/image.pug'
    require_parent = True
    parent_classes = ['GalleryCMSPlugin']


class HtmlCMSPlugin(CMSPluginBase):
    name = _('HTML')
    model = HtmlPlugin
    render_template = 'cms_plugins/html.pug'


class ContentCMSPlugin(CMSPluginBase):
    name = _('Content')
    model = ContentPlugin
    render_template = 'cms_plugins/content.pug'
    allow_children = True


plugin_pool.register_plugin(GalleryCMSPlugin)
plugin_pool.register_plugin(ImageCMSPlugin)
plugin_pool.register_plugin(HtmlCMSPlugin)
plugin_pool.register_plugin(ContentCMSPlugin)
