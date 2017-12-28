# -*- coding: utf-8 -*-
""" Views for the ministries application. """
# standard library

# django
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

# models
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Region


class InstitutionListView(TemplateView):
    template_name = 'institutions/institution_list.pug'

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data(**kwargs)

        context['ministry_list'] = Ministry.objects.by_government_structure(
            self.request.government_structure
        ).prefetch_related('translations')

        context['public_service_list'] = PublicService.objects.filter(
            ministry__government_structure=self.request.government_structure
        ).prefetch_related('translations')

        context['region_list'] = Region.objects.by_government_structure(
            self.request.government_structure
        ).prefetch_related('translations')

        context['title'] = _('Institutions')

        return context
