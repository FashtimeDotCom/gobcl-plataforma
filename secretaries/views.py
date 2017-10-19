# -*- coding: utf-8 -*-
""" Views for the secretaries application. """
# standard library

# django

# models
from .models import Secretary

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import SecretaryForm


class SecretaryListView(BaseListView):
    """
    View for displaying a list of secretaries.
    """
    model = Secretary
    template_name = 'secretaries/secretary_list.pug'
    permission_required = 'secretaries.view_secretary'

    def get_queryset(self):
        queryset = super(SecretaryListView, self).get_queryset()
        queryset = queryset.by_government_structure(self.request.government)
        return queryset


class SecretaryCreateView(BaseCreateView):
    """
    A view for creating a single secretary
    """
    model = Secretary
    form_class = SecretaryForm
    template_name = 'secretaries/secretary_create.pug'
    permission_required = 'secretaries.add_secretary'


class SecretaryDetailView(BaseDetailView):
    """
    A view for displaying a single secretary
    """
    model = Secretary
    template_name = 'secretaries/secretary_detail.pug'
    permission_required = 'secretaries.view_secretary'

    def get_queryset(self):
        queryset = super(SecretaryDetailView, self).get_queryset()
        queryset = queryset.by_government_structure(self.request.government)
        return queryset


class SecretaryUpdateView(BaseUpdateView):
    """
    A view for editing a single secretary
    """
    model = Secretary
    form_class = SecretaryForm
    template_name = 'secretaries/secretary_update.pug'
    permission_required = 'secretaries.change_secretary'


class SecretaryDeleteView(BaseDeleteView):
    """
    A view for deleting a single secretary
    """
    model = Secretary
    permission_required = 'secretaries.delete_secretary'
    template_name = 'secretaries/secretary_delete.pug'
