# -*- coding: utf-8 -*-
""" Views for the governments application. """
# standard library

# django

# models
from .models import Government

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import GovernmentForm


class GovernmentListView(BaseListView):
    """
    View for displaying a list of governments.
    """
    model = Government
    template_name = 'governments/list.pug'
    permission_required = 'governments.view_government'


class GovernmentCreateView(BaseCreateView):
    """
    A view for creating a single government
    """
    model = Government
    form_class = GovernmentForm
    template_name = 'governments/create.pug'
    permission_required = 'governments.add_government'


class GovernmentDetailView(BaseDetailView):
    """
    A view for displaying a single government
    """
    model = Government
    template_name = 'governments/detail.pug'
    permission_required = 'governments.view_government'


class GovernmentUpdateView(BaseUpdateView):
    """
    A view for editing a single government
    """
    model = Government
    form_class = GovernmentForm
    template_name = 'governments/update.pug'
    permission_required = 'governments.change_government'


class GovernmentDeleteView(BaseDeleteView):
    """
    A view for deleting a single government
    """
    model = Government
    permission_required = 'governments.delete_government'
    template_name = 'governments/delete.pug'
