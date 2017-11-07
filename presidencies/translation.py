from modeltranslation.translator import translator, TranslationOptions
from presidencies.models import PresidencyURL
from presidencies.models import Presidency


class PresidencyURLTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(PresidencyURL, PresidencyURLTranslationOptions)


class PresidencyTranslationOptions(TranslationOptions):
    fields = ('name', 'title', 'description')


translator.register(Presidency, PresidencyTranslationOptions)
