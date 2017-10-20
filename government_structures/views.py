# -*- coding: utf-8 -*-
""" Views for the government_structures application. """
# standard library

# django

# models
from .models import GovernmentStructure

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import GovernmentStructureForm


class GovernmentStructureListView(BaseListView):
    """
    View for displaying a list of government_structures.
    """
    model = GovernmentStructure
    template_name = 'government_structures/governmentstructure_list.pug'
    permission_required = 'government_structures.view_government_structure'


class GovernmentStructureCreateView(BaseCreateView):
    """
    A view for creating a single government_structure
    """
    model = GovernmentStructure
    form_class = GovernmentStructureForm
    template_name = 'government_structures/governmentstructure_create.pug'
    permission_required = 'government_structures.add_government_structure'


class GovernmentStructureDetailView(BaseDetailView):
    """
    A view for displaying a single government_structure
    """
    model = GovernmentStructure
    template_name = 'government_structures/governmentstructure_detail.pug'
    permission_required = 'government_structures.view_government_structure'


class GovernmentStructureUpdateView(BaseUpdateView):
    """
    A view for editing a single government_structure
    """
    model = GovernmentStructure
    form_class = GovernmentStructureForm
    template_name = 'government_structures/governmentstructure_update.pug'
    permission_required = 'government_structures.change_government_structure'


class GovernmentStructureDeleteView(BaseDeleteView):
    """
    A view for deleting a single government_structure
    """
    model = GovernmentStructure
    permission_required = 'government_structures.delete_government_structure'
    template_name = 'government_structures/governmentstructure_delete.pug'
