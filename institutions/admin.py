# -*- coding: utf-8 -*-
""" Administration classes for the institutions application. """
# django
from django.contrib import admin
from django.utils.encoding import force_text

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin


class GovernmentStructureFilter(admin.RelatedOnlyFieldListFilter):

    def choices(self, changelist):
        for pk_val, val in self.lookup_choices:
            yield {
                'selected': self.lookup_val == force_text(pk_val),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: pk_val,
                }, [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if self.include_empty_choice:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }


class InstitutionAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'government_structure',
        'url',
    )
    search_fields = (
        'translations__name',
        'url',
        'translations__description',
    )
    list_filter = (
        ('government_structure', GovernmentStructureFilter),
    )
