# -*- coding: utf-8 -*-
""" Views for the contingencies application. """
# standard library

# django

# models
from .models import Contingency

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import ContingencyForm


class ContingencyListView(BaseListView):
    """
    View for displaying a list of contingencies.
    """
    model = Contingency
    template_name = 'contingencies/contingency_list.pug'
    permission_required = 'contingencies.view_contingency'


class ContingencyCreateView(BaseCreateView):
    """
    A view for creating a single contingency
    """
    model = Contingency
    form_class = ContingencyForm
    template_name = 'contingencies/contingency_create.pug'
    permission_required = 'contingencies.add_contingency'


class ContingencyDetailView(BaseDetailView):
    """
    A view for displaying a single contingency
    """
    model = Contingency
    template_name = 'contingencies/contingency_detail.pug'
    permission_required = 'contingencies.view_contingency'


class ContingencyUpdateView(BaseUpdateView):
    """
    A view for editing a single contingency
    """
    model = Contingency
    form_class = ContingencyForm
    template_name = 'contingencies/contingency_update.pug'
    permission_required = 'contingencies.change_contingency'


class ContingencyDeleteView(BaseDeleteView):
    """
    A view for deleting a single contingency
    """
    model = Contingency
    permission_required = 'contingencies.delete_contingency'
    template_name = 'contingencies/contingency_delete.pug'
