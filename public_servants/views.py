# -*- coding: utf-8 -*-
""" Views for the public_servants application. """
# standard library

# django

# models
from .models import PublicServant

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import PublicServantForm


class PublicServantListView(BaseListView):
    """
    View for displaying a list of public_servants.
    """
    model = PublicServant
    template_name = 'public_servants/list.pug'
    permission_required = 'public_servants.view_public_servant'


class PublicServantCreateView(BaseCreateView):
    """
    A view for creating a single public_servant
    """
    model = PublicServant
    form_class = PublicServantForm
    template_name = 'public_servants/create.pug'
    permission_required = 'public_servants.add_public_servant'


class PublicServantDetailView(BaseDetailView):
    """
    A view for displaying a single public_servant
    """
    model = PublicServant
    template_name = 'public_servants/detail.pug'
    permission_required = 'public_servants.view_public_servant'


class PublicServantUpdateView(BaseUpdateView):
    """
    A view for editing a single public_servant
    """
    model = PublicServant
    form_class = PublicServantForm
    template_name = 'public_servants/update.pug'
    permission_required = 'public_servants.change_public_servant'


class PublicServantDeleteView(BaseDeleteView):
    """
    A view for deleting a single public_servant
    """
    model = PublicServant
    permission_required = 'public_servants.delete_public_servant'
    template_name = 'public_servants/delete.pug'
