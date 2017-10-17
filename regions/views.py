# -*- coding: utf-8 -*-
""" Views for the regions application. """
# standard library

# django

# models
from .models import Region

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

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
    template_name = 'regions/create.pug'
    permission_required = 'regions.add_region'


class RegionDetailView(BaseDetailView):
    """
    A view for displaying a single region
    """
    model = Region
    template_name = 'regions/detail.pug'
    permission_required = 'regions.view_region'


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
