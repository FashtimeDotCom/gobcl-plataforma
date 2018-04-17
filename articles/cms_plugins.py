# -*- coding: utf-8 -*-
""" Plugins for the articles application. """
# standard library

# django
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

# models
from cms.models.pluginmodel import CMSPlugin
from .models import Article


class FeaturedArticleCMSPlugin(CMSPluginBase):
    name = _('Featured Article')
    model = CMSPlugin
    render_template = 'cms_plugins/featured_article.pug'

    def render(self, context, instance, placeholder):
        context = super(FeaturedArticleCMSPlugin, self).render(
            context, instance, placeholder
        )
        context['article'] = Article.objects.filter(is_featured=True).first()
        return context


plugin_pool.register_plugin(FeaturedArticleCMSPlugin)
