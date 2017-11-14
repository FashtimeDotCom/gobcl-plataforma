from modeltranslation.translator import translator, TranslationOptions
from ministries.models import PublicService
from ministries.models import Ministry


class MinistryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug')


translator.register(Ministry, MinistryTranslationOptions)


class PublicServiceTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(PublicService, PublicServiceTranslationOptions)
