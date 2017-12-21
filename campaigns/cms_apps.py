# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class CampaignApp(CMSConfigApp):
    app_name = 'campaigns'
    name = _('Campaigns')

    def get_urls(self, page=None, language=None, **kwargs):
        # replace this with the path to your application's URLs module
        return ['campaigns.urls']


apphook_pool.register(CampaignApp)
