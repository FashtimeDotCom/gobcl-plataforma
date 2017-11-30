from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from .models import Campaign


class CampaignTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
    )


translator.register(Campaign, CampaignTranslationOptions)
