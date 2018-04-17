from django.utils.translation import ugettext_lazy as _

from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from .forms import ArticleForm


class ArticleWizard(Wizard):
    pass


article_wizard = ArticleWizard(
    title=_('New Article'),
    weight=200,
    form=ArticleForm,
    description=_('Create a new Article'),
)

wizard_pool.register(article_wizard)
