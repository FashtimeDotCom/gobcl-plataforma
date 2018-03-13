# -*- coding: utf-8 -*-
""" Administration classes for the ministries application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from institutions.admin import InstitutionAdmin
from institutions.admin import GovernmentStructureFilter

# parler
from parler.admin import TranslatableAdmin

# Aldryn
from aldryn_translation_tools.admin import AllTranslationsMixin

# models
from .models import Ministry, PublicService
from public_servants.models import PublicServant


@admin.register(Ministry)
class MinistryAdmin(InstitutionAdmin):
    list_display = (
        'name',
        'government_structure',
        'minister',
        'url',
    )

    filter_horizontal = (
        'public_servants',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related().prefetch_related(
            'translations',
            'public_servants',
        )
        return qs

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:ministries_ministry_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)

    def render_change_form(self, request, context, *args, **kwargs):
        form = context['adminform'].form
        fields = form.fields
        public_servants = PublicServant.objects.filter(
            government_structure_id=form.instance.government_structure_id
        )
        fields['minister'].queryset = public_servants
        fields['public_servants'].queryset = public_servants
        return super(MinistryAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


@admin.register(PublicService)
class PublicServiceAdmin(AllTranslationsMixin, TranslatableAdmin):
    list_filter = (
        ('ministry__government_structure', GovernmentStructureFilter),
    )
    list_display = (
        'name',
        'ministry',
        'url',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related().prefetch_related(
            'translations', 'ministry__translations',)
        return qs

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('ministry__government_structure__id__exact'):
            return redirect(
                reverse('admin:ministries_publicservice_changelist') +
                '?ministry__government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)
