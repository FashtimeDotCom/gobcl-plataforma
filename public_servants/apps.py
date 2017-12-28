from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PublicServantsConfig(AppConfig):
    name = 'public_servants'
    verbose_name = _('public servants')
