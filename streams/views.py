# -*- coding: utf-8 -*-
""" Views for the streams application. """
# standard library

# django

# models
from .models import Stream

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from django.views.generic import DetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import StreamForm


class StreamListView(BaseListView):
    """
    View for displaying a list of streams.
    """
    model = Stream
    template_name = 'streams/stream_list.pug'
    permission_required = 'streams.view_stream'


class StreamCreateView(BaseCreateView):
    """
    A view for creating a single stream
    """
    model = Stream
    form_class = StreamForm
    template_name = 'streams/stream_create.pug'
    permission_required = 'streams.add_stream'


class StreamDetailView(DetailView):
    """
    A view for displaying a single stream
    """
    model = Stream
    template_name = 'streams/stream_detail.pug'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('events').active()
        return queryset


class StreamUpdateView(BaseUpdateView):
    """
    A view for editing a single stream
    """
    model = Stream
    form_class = StreamForm
    template_name = 'streams/stream_update.pug'
    permission_required = 'streams.change_stream'


class StreamDeleteView(BaseDeleteView):
    """
    A view for deleting a single stream
    """
    model = Stream
    permission_required = 'streams.delete_stream'
    template_name = 'streams/stream_delete.pug'
