from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PublicEnterprisesConfig(AppConfig):
    name = 'public_enterprises'
    verbose_name = _('public enterprises')
