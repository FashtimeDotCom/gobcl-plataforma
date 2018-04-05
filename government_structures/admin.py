# -*- coding: utf-8 -*-
""" Administration classes for the government_structures application. """
# standard library

# django
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ugettext as _

# models
from .models import GovernmentStructure


@admin.register(GovernmentStructure)
class GovernmentStructureAdmin(admin.ModelAdmin):
    list_display = (
        'publication_date',
        'current_government',
        'copy_actions',
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<gov_id>.+)/copy-structure/$',
                self.admin_site.admin_view(
                    self.copy_structure
                ),
                name='copy',
            ),
            url(
                r'^(?P<gov_id>.+)/copy-structure/servants/$',
                self.admin_site.admin_view(
                    self.copy_structure_without_servants
                ),
                name='copy_servants',
            ),
        ]
        return custom_urls + urls

    def copy_structure(self, request, gov_id):
        gov = GovernmentStructure.objects.get(pk=gov_id)
        gov.duplicate(date=timezone.now())
        url = reverse(
            'admin:government_structures_governmentstructure_change',
            args=[gov.pk],
            current_app=self.admin_site.name,
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            _('government structure copy succesful'),
        )
        return HttpResponseRedirect(url)

    def copy_structure_without_servants(self, request, gov_id):
        gov = GovernmentStructure.objects.get(pk=gov_id)
        gov.duplicate(date=timezone.now(), with_public_servants=False)
        url = reverse(
            'admin:government_structures_governmentstructure_change',
            args=[gov.pk],
            current_app=self.admin_site.name,
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            _('new government structure succesful'),
        )
        return HttpResponseRedirect(url)

    def copy_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">' + _(
                'copy government'
            ).capitalize() + '</a>&nbsp;'
            '<a class="button" href="{}">' + _(
                'new government'
            ).capitalize() + '</a>',
            reverse('admin:copy', args=[obj.pk]),
            reverse('admin:copy_servants', args=[obj.pk]),
        )

    copy_structure.allow_tags = True
    copy_structure.short_description = _('copy structure')

    copy_structure_without_servants.allow_tags = True
    copy_structure_without_servants.short_description = _(
        'copy without servants'
    )
