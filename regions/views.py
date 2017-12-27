# -*- coding: utf-8 -*-
""" Views for the regions application. """
# standard library

# django
from django.urls import reverse

# models
from .models import Region
from .models import Commune

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseListView
from base.views import BaseUpdateView
from base.views import BaseSubModelCreateView
from parler.views import TranslatableSlugMixin

from hitcount.views import HitCountDetailView

# forms
from .forms import RegionForm
from .forms import CommuneForm


class RegionListView(BaseListView):
    """
    View for displaying a list of regions.
    """
    model = Region
    template_name = 'regions/region_list.pug'
    permission_required = 'regions.view_region'


class RegionCreateView(BaseCreateView):
    """
    A view for creating a single region
    """
    model = Region
    form_class = RegionForm
    template_name = 'regions/region_create.pug'
    permission_required = 'regions.add_region'

    def get_form_kwargs(self):
        kwargs = super(RegionCreateView, self).get_form_kwargs()
        kwargs['instance'] = Region(
            government_structure=self.request.government_structure,
        )
        return kwargs

    def get_cancel_url(self):
        return reverse('institution_list')

    def get_success_url(self):
        return reverse('institution_list')


class RegionDetailView(TranslatableSlugMixin, HitCountDetailView):
    """
    A view for displaying a single region
    """
    model = Region
    template_name = 'regions/region_detail.pug'
    count_hit = True

    def get_queryset(self):
        queryset = super(RegionDetailView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset.prefetch_related('commune_set',)


class RegionUpdateView(BaseUpdateView):
    """
    A view for editing a single region
    """
    model = Region
    form_class = RegionForm
    template_name = 'regions/region_update.pug'
    permission_required = 'regions.change_region'


class RegionDeleteView(BaseDeleteView):
    """
    A view for deleting a single region
    """
    model = Region
    permission_required = 'regions.delete_region'
    template_name = 'regions/region_delete.pug'

    def get_success_url(self):
        return reverse('institution_list')


class CommuneListView(BaseListView):
    """
    View for displaying a list of communes.
    """
    model = Commune
    template_name = 'communes/commune_list.pug'
    permission_required = 'regions.view_commune'

    def get_region(self):
        return Region.objects.get(
            translations__slug=self.kwargs['region_slug'],
        )

    def get_queryset(self):
        queryset = super(CommuneListView, self).get_queryset()
        return queryset.filter(region=self.get_region())

    def get_context_data(self, **kwargs):
        context = super(CommuneListView, self).get_context_data(**kwargs)
        region = Region.objects.get(
            translations__slug=self.kwargs['region_slug'],
        )
        context.update(
            {
                'region': region,
            }
        )
        return context


class CommuneCreateView(BaseSubModelCreateView):
    """
    A view for creating a single commune
    """
    model = Commune
    parent_model = Region
    form_class = CommuneForm
    template_name = 'communes/commune_create.pug'
    permission_required = 'regions.add_commune'

    def get_region(self):
        return Region.objects.get(
            translations__slug=self.kwargs['region_slug'],
        )

    def get_form_kwargs(self):
        kwargs = super(CommuneCreateView, self).get_form_kwargs()
        kwargs['instance'] = Commune(
            region=self.get_region(),
        )
        return kwargs

    def get_cancel_url(self):
        return reverse('region_detail', args=(self.region.slug,))


class CommuneUpdateView(BaseUpdateView):
    """
    A view for editing a single commune
    """
    model = Commune
    form_class = CommuneForm
    template_name = 'communes/commune_update.pug'
    permission_required = 'regions.change_commune'

    def get_cancel_url(self):
        return reverse('region_detail', args=(self.object.region.slug,))

    def get_success_url(self):
        return reverse('region_detail', args=(self.object.region.slug,))


class CommuneDeleteView(BaseDeleteView):
    """
    A view for deleting a single commune
    """
    model = Commune
    permission_required = 'regions.delete_commune'
    template_name = 'communes/commune_delete.pug'

    def get_cancel_url(self):
        return reverse('region_detail', args=(self.object.region.slug,))

    def get_success_url(self):
        return reverse('region_detail', args=(self.object.region.slug,))
