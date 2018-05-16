# -*- coding: utf-8 -*-
""" CMSAppConfig for the articles application. """

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class ArticleApp(CMSApp):
    app_name = 'articles'
    name = _('Articles')

    def get_urls(self, page=None, language=None, **kwargs):
        return ['articles.urls']
