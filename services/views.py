# -*- coding: utf-8 -*-
""" Views for the services application. """
# standard library

# django
from django.conf import settings
from django.http import JsonResponse

# models
from .models import ChileAtiendeService

# views
from base.views import BaseDeleteView
from base.views import BaseDetailView
from django.views.generic import ListView
from django.views.generic import View

# chile atiende client
from .chile_atiende_client import File


class ChileAtiendeServiceListView(ListView):
    """
    View for displaying a list of Chile Atiende Services.
    """
    model = ChileAtiendeService
    template_name = 'services/service_list.pug'
    paginate_by = 9

    def get_queryset(self):
        queryset = super(ChileAtiendeServiceListView, self).get_queryset()

        queryset = queryset.prefetch_related('files')

        return queryset


class FileSearchJson(View):

    def dispatch(self, request, *args, **kwargs):
        self.query = self.request.GET.get('query', '')
        return super(
            FileSearchJson, self).dispatch(request, *args, **kwargs)

    def get_file_list(self):
        file_data = File()

        if self.request.GET.get('q'):
            if settings.CHILEATIENDE_ACCESS_TOKEN:
                return file_data.list(query=self.query).json()

        # return empty json object
        return '{}'

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_file_list(), safe=False)


class ServiceDetailView(BaseDetailView):
    """
    A view for displaying a single service
    """
    model = ChileAtiendeService
    template_name = 'services/service_detail.pug'
    permission_required = 'services.view_service'


class ServiceDeleteView(BaseDeleteView):
    """
    A view for deleting a single service
    """
    model = ChileAtiendeService
    permission_required = 'services.delete_service'
    template_name = 'services/service_delete.pug'
