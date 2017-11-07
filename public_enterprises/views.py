# -*- coding: utf-8 -*-
""" Views for the public_enterprises application. """
# standard library

# django

# models
from .models import PublicEnterprise

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import PublicEnterpriseForm


class PublicEnterpriseListView(BaseListView):
    """
    View for displaying a list of public_enterprises.
    """
    model = PublicEnterprise
    template_name = 'public_enterprises/public_enterprise_list.pug'
    permission_required = 'public_enterprises.view_public_enterprise'


class PublicEnterpriseCreateView(BaseCreateView):
    """
    A view for creating a single public_enterprise
    """
    model = PublicEnterprise
    form_class = PublicEnterpriseForm
    template_name = 'public_enterprises/public_enterprise_create.pug'
    permission_required = 'public_enterprises.add_public_enterprise'


class PublicEnterpriseDetailView(BaseDetailView):
    """
    A view for displaying a single public_enterprise
    """
    model = PublicEnterprise
    template_name = 'public_enterprises/public_enterprise_detail.pug'
    permission_required = 'public_enterprises.view_public_enterprise'


class PublicEnterpriseUpdateView(BaseUpdateView):
    """
    A view for editing a single public_enterprise
    """
    model = PublicEnterprise
    form_class = PublicEnterpriseForm
    template_name = 'public_enterprises/public_enterprise_update.pug'
    permission_required = 'public_enterprises.change_public_enterprise'


class PublicEnterpriseDeleteView(BaseDeleteView):
    """
    A view for deleting a single public_enterprise
    """
    model = PublicEnterprise
    permission_required = 'public_enterprises.delete_public_enterprise'
    template_name = 'public_enterprises/public_enterprise_delete.pug'
