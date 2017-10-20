# -*- coding: utf-8 -*-
""" Views for the presidencies application. """
# standard library

# django

# models
from .models import Presidency

# views
from base.views import BaseDetailView


class PresidencyDetailView(BaseDetailView):
    """
    A view for displaying a single presidency
    """
    model = Presidency
    template_name = 'presidencies/presidency_detail.pug'

    def get_queryset(self):
        queryset = super(PresidencyDetailView, self).get_queryset()
        queryset = queryset.by_government_structure(
            self.request.government_structure)
        return queryset
