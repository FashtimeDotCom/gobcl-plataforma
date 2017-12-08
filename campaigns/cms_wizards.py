from django.utils.translation import ugettext_lazy as _

from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from .forms import CampaignForm


class CampaignWizard(Wizard):
    pass


campaign_wizard = CampaignWizard(
    title=_('Campaign'),
    weight=200,
    form=CampaignForm,
    description=_('Create a new Campaign'),
)

wizard_pool.register(campaign_wizard)
