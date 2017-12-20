# -*- coding: utf-8 -*-
""" Views for the ministries application. """
# standard library

# django
from django.urls import reverse

# models
from .models import Ministry
from .models import PublicService

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseListView
from base.views import BaseUpdateView
from hitcount.views import HitCountDetailView
from parler.views import TranslatableSlugMixin

# forms
from .forms import MinistryForm
from .forms import PublicServiceForm


class MinistryListView(BaseListView):
    """
    View for displaying a list of ministries.
    """
    model = Ministry
    template_name = 'ministries/ministry_list.pug'

    def get_queryset(self):
        queryset = super(MinistryListView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset


class MinistryCreateView(BaseCreateView):
    """
    A view for creating a single ministry
    """
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_create.pug'
    permission_required = 'ministries.add_ministry'

    def get_success_url(self):
        return reverse('institution_list')

    def get_cancel_url(self):
        return reverse('institution_list')


class MinistryDetailView(TranslatableSlugMixin, HitCountDetailView):
    """
    A view for displaying a single ministry
    """
    model = Ministry
    template_name = 'ministries/ministry_detail.pug'
    count_hit = True
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super(MinistryDetailView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset


class MinistryUpdateView(BaseUpdateView):
    """
    A view for editing a single ministry
    """
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_update.pug'
    permission_required = 'ministries.change_ministry'


class MinistryDeleteView(BaseDeleteView):
    """
    A view for deleting a single ministry
    """
    model = Ministry
    permission_required = 'ministries.delete_ministry'
    template_name = 'ministries/ministry_delete.pug'

    def get_success_url(self):
        return reverse('institution_list')


class PublicServiceListView(BaseListView):
    """
    View for displaying a list of ministries.
    """
    model = PublicService
    template_name = 'ministries/ministry_list.pug'

    def get_queryset(self):
        queryset = super(PublicServiceListView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset


class PublicServiceCreateView(BaseCreateView):
    """
    A view for creating a single ministry
    """
    model = PublicService
    form_class = PublicServiceForm
    template_name = 'ministries/ministry_create.pug'
    permission_required = 'ministries.add_publicservice'

    def get_success_url(self):
        return reverse('institution_list')

    def get_cancel_url(self):
        return reverse('institution_list')


class PublicServiceUpdateView(BaseUpdateView):
    """
    A view for editing a single ministry
    """
    model = PublicService
    form_class = PublicServiceForm
    template_name = 'ministries/ministry_update.pug'
    permission_required = 'ministries.change_publicservice'


class PublicServiceDeleteView(BaseDeleteView):
    """
    A view for deleting a single ministry
    """
    model = PublicService
    permission_required = 'ministries.delete_publicservice'
    template_name = 'ministries/ministry_delete.pug'
    # success url de institutions list
