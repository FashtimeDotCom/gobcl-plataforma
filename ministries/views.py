# -*- coding: utf-8 -*-
""" Views for the ministries application. """
# standard library

# django

# models
from .models import Ministry

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import MinistryForm


class MinistryListView(BaseListView):
    """
    View for displaying a list of ministries.
    """
    model = Ministry
    template_name = 'ministries/ministry_list.pug'
    permission_required = 'ministries.view_ministry'

    def get_queryset(self):
        queryset = super(MinistryListView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset


class MinistryCreateView(BaseCreateView):
    """
    A view for creating a single ministry
    """
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_create.pug'
    permission_required = 'ministries.add_ministry'


class MinistryDetailView(BaseDetailView):
    """
    A view for displaying a single ministry
    """
    model = Ministry
    template_name = 'ministries/ministry_detail.pug'
    permission_required = 'ministries.view_ministry'

    def get_queryset(self):
        queryset = super(MinistryDetailView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset


class MinistryUpdateView(BaseUpdateView):
    """
    A view for editing a single ministry
    """
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_update.pug'
    permission_required = 'ministries.change_ministry'


class MinistryDeleteView(BaseDeleteView):
    """
    A view for deleting a single ministry
    """
    model = Ministry
    permission_required = 'ministries.delete_ministry'
    template_name = 'ministries/ministry_delete.pug'
