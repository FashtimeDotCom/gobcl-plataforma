# -*- coding: utf-8 -*-
""" Administration classes for the contingencies application. """
# standard library

# django
from django.contrib import admin

from aldryn_translation_tools.admin import AllTranslationsMixin

from parler.admin import TranslatableAdmin
from parler.admin import TranslatableTabularInline

# models
from .models import Contingency
from .models import ContingencyEvent
from .models import ContingencyInformation


class ContingencyEventInline(TranslatableTabularInline):
    model = ContingencyEvent


class ContingencyInformationInline(TranslatableTabularInline):
    model = ContingencyInformation


@admin.register(Contingency)
class ContingencyAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'name',
        'is_active',
        'created_at',
    )
    search_fields = (
        'translations__name',
        'translations__lead',
        'translations__description',
    )
    list_filter = (
        'is_active',
    )

    inlines = (ContingencyEventInline, ContingencyInformationInline)


@admin.register(ContingencyEvent)
class ContingencyEventAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'title',
        'contingency',
        'date_time',
    )
    search_fields = (
        'translations__title',
    )
    list_filter = (
        'contingency',
    )


@admin.register(ContingencyInformation)
class ContingencyInformationAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_display = (
        'title',
        'contingency',
        'url',
    )
    search_fields = (
        'translations__title',
        'translations__description',
    )
    list_filter = (
        'contingency',
    )
