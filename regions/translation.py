from modeltranslation.translator import translator, TranslationOptions
from regions.models import Region
from regions.models import Commune


class RegionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Region, RegionTranslationOptions)


class CommuneTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Commune, CommuneTranslationOptions)
