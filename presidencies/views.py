# -*- coding: utf-8 -*-
""" Views for the presidencies application. """
# standard library

# django

# models
from .models import Presidency

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseUpdateView

# forms
from .forms import PresidencyForm


class PresidencyCreateView(BaseCreateView):
    """
    A view for creating a single presidency
    """
    model = Presidency
    form_class = PresidencyForm
    template_name = 'presidencies/presidency_create.pug'
    permission_required = 'presidencies.add_presidency'


class PresidencyDetailView(BaseDetailView):
    """
    A view for displaying a single presidency
    """
    model = Presidency
    template_name = 'presidencies/presidency_detail.pug'

    def get_object(self, queryset=None):
        print(self.request.government_structure, self.request.government_structure.id)
        return self.request.government_structure.presidency


class PresidencyUpdateView(BaseUpdateView):
    """
    A view for editing a single presidency
    """
    model = Presidency
    form_class = PresidencyForm
    template_name = 'presidencies/presidency_update.pug'
    permission_required = 'presidencies.change_presidency'


class PresidencyDeleteView(BaseDeleteView):
    """
    A view for deleting a single presidency
    """
    model = Presidency
    permission_required = 'presidencies.delete_presidency'
    template_name = 'presidencies/presidency_delete.pug'
