# -*- coding: utf-8 -*-
""" Views for the services application. """
# standard library

# django

# models
from .models import Service

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseUpdateView
from django.views.generic import ListView

# forms
from .forms import ServiceForm


class ServiceListView(ListView):
    """
    View for displaying a list of services.
    """
    model = Service
    template_name = 'services/service_list.pug'
    paginate_by = 9

    def get_queryset(self):
        queryset = super(ServiceListView, self).get_queryset()

        queryset = queryset.prefetch_related('files')

        return queryset


class ServiceCreateView(BaseCreateView):
    """
    A view for creating a single service
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_create.pug'
    permission_required = 'services.add_service'


class ServiceDetailView(BaseDetailView):
    """
    A view for displaying a single service
    """
    model = Service
    template_name = 'services/service_detail.pug'
    permission_required = 'services.view_service'


class ServiceUpdateView(BaseUpdateView):
    """
    A view for editing a single service
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_update.pug'
    permission_required = 'services.change_service'


class ServiceDeleteView(BaseDeleteView):
    """
    A view for deleting a single service
    """
    model = Service
    permission_required = 'services.delete_service'
    template_name = 'services/service_delete.pug'
