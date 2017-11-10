# -*- coding: utf-8 -*-
""" Views for the regions application. """
# standard library

# models
from .models import Region

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseListView
from base.views import BaseUpdateView

from hitcount.views import HitCountDetailView

# forms
from .forms import RegionForm


class RegionListView(BaseListView):
    """
    View for displaying a list of regions.
    """
    model = Region
    template_name = 'regions/list.pug'
    permission_required = 'regions.view_region'


class RegionCreateView(BaseCreateView):
    """
    A view for creating a single region
    """
    model = Region
    form_class = RegionForm
    template_name = 'regions/region_create.pug'
    permission_required = 'regions.add_region'


class RegionDetailView(HitCountDetailView):
    """
    A view for displaying a single region
    """
    model = Region
    template_name = 'regions/region_detail.pug'
    count_hit = True

    def get_slug_field(self):
        return "slug_{}".format(self.request.LANGUAGE_CODE)

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
    template_name = 'regions/update.pug'
    permission_required = 'regions.change_region'


class RegionDeleteView(BaseDeleteView):
    """
    A view for deleting a single region
    """
    model = Region
    permission_required = 'regions.delete_region'
    template_name = 'regions/delete.pug'
