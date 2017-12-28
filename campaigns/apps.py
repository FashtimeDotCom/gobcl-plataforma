from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CampaignsConfig(AppConfig):
    verbose_name = _('campaigns')
    name = 'campaigns'
