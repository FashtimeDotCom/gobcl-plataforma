# -*- coding: utf-8 -*-
""" Views for the campaigns application. """
# standard library

# django

# models
from .models import Campaign

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseUpdateView
from django.views.generic import ListView

# forms
from .forms import CampaignForm


class CampaignListView(ListView):
    """
    View for displaying a list of campaigns.
    """
    model = Campaign
    template_name = 'campaigns/campaign_list.pug'
    paginate_by = 25


class CampaignCreateView(BaseCreateView):
    """
    A view for creating a single campaign
    """
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign_create.pug'
    permission_required = 'campaigns.add_campaign'


class CampaignDetailView(BaseDetailView):
    """
    A view for displaying a single campaign
    """
    model = Campaign
    template_name = 'campaigns/campaign_detail.pug'
    permission_required = 'campaigns.view_campaign'


class CampaignUpdateView(BaseUpdateView):
    """
    A view for editing a single campaign
    """
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign_update.pug'
    permission_required = 'campaigns.change_campaign'


class CampaignDeleteView(BaseDeleteView):
    """
    A view for deleting a single campaign
    """
    model = Campaign
    permission_required = 'campaigns.delete_campaign'
    template_name = 'campaigns/campaign_delete.pug'
