# -*- coding: utf-8 -*-
""" Views for the links application. """
# standard library

# django

# models
from .models import Link

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import LinkForm


class LinkListView(BaseListView):
    """
    View for displaying a list of links.
    """
    model = Link
    template_name = 'links/link_list.pug'
    permission_required = 'links.view_link'


class LinkCreateView(BaseCreateView):
    """
    A view for creating a single link
    """
    model = Link
    form_class = LinkForm
    template_name = 'links/link_create.pug'
    permission_required = 'links.add_link'


class LinkDetailView(BaseDetailView):
    """
    A view for displaying a single link
    """
    model = Link
    template_name = 'links/link_detail.pug'
    permission_required = 'links.view_link'


class LinkUpdateView(BaseUpdateView):
    """
    A view for editing a single link
    """
    model = Link
    form_class = LinkForm
    template_name = 'links/link_update.pug'
    permission_required = 'links.change_link'


class LinkDeleteView(BaseDeleteView):
    """
    A view for deleting a single link
    """
    model = Link
    permission_required = 'links.delete_link'
    template_name = 'links/link_delete.pug'
