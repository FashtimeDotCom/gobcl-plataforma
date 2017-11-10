from modeltranslation.translator import translator, TranslationOptions
from public_enterprises.models import PublicEnterprise


class PublicEnterpriseURLTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(PublicEnterprise, PublicEnterpriseURLTranslationOptions)
