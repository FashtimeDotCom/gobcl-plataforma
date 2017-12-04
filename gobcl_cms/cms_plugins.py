from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import HtmlPlugin
from .models import ImageGallery
from .models import GalleryPLugin


class ImagePluginInlineAdmin(admin.StackedInline):
    model = ImageGallery


class GalleryCMSPlugin(CMSPluginBase):
    model = GalleryPLugin
    name = _('Gallery')
    render_template = 'cms_plugins/gallery/gallery.pug'
    # child_classes = ('ImageCMSPlugin',)
    allow_children = False
    inlines = (ImagePluginInlineAdmin,)

    def render(self, context, instance, placeholder):
        context = super(GalleryCMSPlugin, self).render(context, instance, placeholder)
        images = instance.imagegallery_set.all()
        context.update({
            'images': images,
        })
        return context


# class ImageCMSPlugin(CMSPluginBase):
#     name = _('Image Gallery')
#     model = ImagePlugin
#     render_plugin = True
#     render = True
#     require_parent = True
#     parent_classes = ('GalleryCMSPlugin',)
#     render_template = 'cms_plugins/gallery/image.pug'


class HtmlCMSPlugin(CMSPluginBase):
    name = _('HTML')
    model = HtmlPlugin
    render_plugin = True
    render_template = 'cms_plugins/html.pug'


plugin_pool.register_plugin(GalleryCMSPlugin)
# plugin_pool.register_plugin(ImageCMSPlugin)
plugin_pool.register_plugin(HtmlCMSPlugin)
