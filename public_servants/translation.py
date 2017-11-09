from modeltranslation.translator import translator, TranslationOptions
from public_servants.models import PublicServant


class PublicServantURLTranslationOptions(TranslationOptions):
    fields = ('charge', 'description')


translator.register(PublicServant, PublicServantURLTranslationOptions)
