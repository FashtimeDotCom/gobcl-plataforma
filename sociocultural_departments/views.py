# -*- coding: utf-8 -*-
""" Views for the sociocultural_departments application. """
# standard library

# django

# models
from .models import SocioculturalDepartment

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import SocioculturalDepartmentForm


class SocioculturalDepartmentListView(BaseListView):
    """
    View for displaying a list of sociocultural_departments.
    """
    model = SocioculturalDepartment
    template_name = 'sociocultural_departments/sociocultural_department_list.pug'
    permission_required = 'sociocultural_departments.view_sociocultural_department'


class SocioculturalDepartmentCreateView(BaseCreateView):
    """
    A view for creating a single sociocultural_department
    """
    model = SocioculturalDepartment
    form_class = SocioculturalDepartmentForm
    template_name = 'sociocultural_departments/sociocultural_department_create.pug'
    permission_required = 'sociocultural_departments.add_sociocultural_department'


class SocioculturalDepartmentDetailView(BaseDetailView):
    """
    A view for displaying a single sociocultural_department
    """
    model = SocioculturalDepartment
    template_name = 'sociocultural_departments/sociocultural_department_detail.pug'

    def get_object(self, queryset=None):
        return self.request.government_structure.socioculturaldepartment


class SocioculturalDepartmentUpdateView(BaseUpdateView):
    """
    A view for editing a single sociocultural_department
    """
    model = SocioculturalDepartment
    form_class = SocioculturalDepartmentForm
    template_name = 'sociocultural_departments/sociocultural_department_update.pug'
    permission_required = 'sociocultural_departments.change_sociocultural_department'


class SocioculturalDepartmentDeleteView(BaseDeleteView):
    """
    A view for deleting a single sociocultural_department
    """
    model = SocioculturalDepartment
    permission_required = 'sociocultural_departments.delete_sociocultural_department'
    template_name = 'sociocultural_departments/sociocultural_department_delete.pug'
