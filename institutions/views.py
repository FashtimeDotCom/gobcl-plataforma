# -*- coding: utf-8 -*-
""" Views for the ministries application. """
# standard library

# django
from django.views.generic import TemplateView

# models
from ministries.models import Ministry
from regions.models import Region
from public_companies.models import PublicCompany


class InstitutionListView(TemplateView):
    template_name = 'institutions/institution_list.pug'

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data(**kwargs)
        context['ministry_list'] = Ministry.objects.by_government_structure(
            self.request.government_structure)
        context['region_list'] = Region.objects.by_government_structure(
            self.request.government_structure)
        context['public_company_list'] = PublicCompany.objects.by_government_structure(
            self.request.government_structure)
        return context
