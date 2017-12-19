# -*- coding: utf-8 -*-
""" Views for the services application. """
# standard library

# django
from django.http import JsonResponse

# models
from .models import Service

# views
from base.views import BaseDeleteView
from base.views import BaseDetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View

# forms
from .chile_atiende_client import File


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


class FileSearchJson(View):

    def dispatch(self, request, *args, **kwargs):
        self.query = self.request.GET.get('query', '')
        return super(
            FileSearchJson, self).dispatch(request, *args, **kwargs)

    def get_file_list(self):
        file_data = File()
        return file_data.list(query=self.query).json()

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_file_list())


class ServiceDetailView(BaseDetailView):
    """
    A view for displaying a single service
    """
    model = Service
    template_name = 'services/service_detail.pug'
    permission_required = 'services.view_service'


class ServiceDeleteView(BaseDeleteView):
    """
    A view for deleting a single service
    """
    model = Service
    permission_required = 'services.delete_service'
    template_name = 'services/service_delete.pug'
