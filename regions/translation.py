from modeltranslation.translator import translator, TranslationOptions
from regions.models import Region


class RegionTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug')


translator.register(Region, RegionTranslationOptions)
