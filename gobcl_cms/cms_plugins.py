from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GalleryImagePlugin, HtmlPlugin
from .models import GalleryPlugin
from .models import HeaderPlugin


class BradcrumCMSPlugin(CMSPluginBase):
    name = _('Breadcrumb')
    model = CMSPlugin
    render_template = 'cms_plugins/breadcrumb.pug'


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


class HeaderCMSPlugin(CMSPluginBase):
    name = _('header')
    model = HeaderPlugin
    render_template = 'cms_plugins/header.pug'


plugin_pool.register_plugin(BradcrumCMSPlugin)
plugin_pool.register_plugin(GalleryCMSPlugin)
plugin_pool.register_plugin(HeaderCMSPlugin)
plugin_pool.register_plugin(HtmlCMSPlugin)
plugin_pool.register_plugin(ImageCMSPlugin)
