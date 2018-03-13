# -*- coding: utf-8 -*-
""" Administration classes for the links application. """
# standard library

# django
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from institutions.admin import GovernmentStructureFilter

from adminsortable2.admin import SortableAdminMixin

# models
from .models import FooterLink


@admin.register(FooterLink)
class FooterLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = (
        ('government_structure', GovernmentStructureFilter),
    )
    list_display = (
        'name',
        'url',
        'government_structure',
    )
    ordering = (
        'order',
    )

    def changelist_view(self, request, extra_content=None):
        if not request.GET.get('government_structure__id__exact'):
            return redirect(
                reverse('admin:links_footerlink_changelist') +
                '?government_structure__id__exact=' +
                str(request.government_structure.pk)
            )
        else:
            return super().changelist_view(request, extra_content)
