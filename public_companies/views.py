# -*- coding: utf-8 -*-
""" Views for the public_companies application. """
# standard library

# django

# models
from .models import PublicCompany

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import PublicCompanyForm


class PublicCompanyListView(BaseListView):
    """
    View for displaying a list of public_companies.
    """
    model = PublicCompany
    template_name = 'public_companies/publiccompany_list.pug'
    permission_required = 'public_companies.view_public_company'


class PublicCompanyCreateView(BaseCreateView):
    """
    A view for creating a single public_company
    """
    model = PublicCompany
    form_class = PublicCompanyForm
    template_name = 'public_companies/publiccompany_create.pug'
    permission_required = 'public_companies.add_public_company'


class PublicCompanyDetailView(BaseDetailView):
    """
    A view for displaying a single public_company
    """
    model = PublicCompany
    template_name = 'public_companies/publiccompany_detail.pug'
    permission_required = 'public_companies.view_public_company'


class PublicCompanyUpdateView(BaseUpdateView):
    """
    A view for editing a single public_company
    """
    model = PublicCompany
    form_class = PublicCompanyForm
    template_name = 'public_companies/publiccompany_update.pug'
    permission_required = 'public_companies.change_public_company'


class PublicCompanyDeleteView(BaseDeleteView):
    """
    A view for deleting a single public_company
    """
    model = PublicCompany
    permission_required = 'public_companies.delete_public_company'
    template_name = 'public_companies/publiccompany_delete.pug'
