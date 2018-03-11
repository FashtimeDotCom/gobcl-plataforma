# -*- coding: utf-8 -*-
""" Administration classes for the regions application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from institutions.admin import InstitutionAdmin

# models
from .models import Region, Commune
from public_servants.models import PublicServant


@admin.register(Region)
class RegionAdmin(InstitutionAdmin):
    list_filter = ('government_structure',)
    list_display = (
        'name',
        'government_structure',
        'governor',
        'url',
    )

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:regions_region_changelist') +
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
        fields['governor'].queryset = public_servants
        return super(RegionAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    list_display = (
        'name',
        'region',
        'email',
        'phone',
        'twitter',
        'url',
    )
