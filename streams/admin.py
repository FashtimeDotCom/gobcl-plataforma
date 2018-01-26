# -*- coding: utf-8 -*-
""" Administration classes for the streams application. """
# standard library

# django
from django.contrib import admin

from parler.admin import TranslatableAdmin
from parler.admin import TranslatableTabularInline

from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Stream
from .models import StreamEvent


class StreamEventInline(TranslatableTabularInline):
    model = StreamEvent


@admin.register(Stream)
class StreamAdmin(AllTranslationsMixin, TranslatableAdmin):
    inlines = (StreamEventInline,)
    list_display = (
        'title',
        'url',
        'is_active',
    )
    list_filter = (
        'is_active',
    )
