from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class StreamApphook(CMSApp):
    app_name = 'stream'
    name = _('stream')

    def get_urls(self, page=None, language=None, **kwargs):
        return ['streams.urls']
