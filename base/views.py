# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library

# external library
from aldryn_newsblog.models import Article

# django
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# utils
from base.view_utils import clean_query_string
from inflection import underscore

# models
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Region
from regions.models import Commune


def index(request):
    """ view that renders a default home"""
    articles = Article.objects.filter(
        is_published=True,
    ).order_by('-publishing_date')[:4]

    context = {
        'procedures_and_benefits': None,
        'campaigns': None,
        'articles': articles,
        'ministries_count': Ministry.objects.count(),
        'public_services_count': PublicService.objects.count(),
        'regions_and_communes_count': (
            Region.objects.count() + Commune.objects.count()
        ),
    }

    return render(request, 'index.pug', context)


def bad_request_view(request):
    return render_to_response('exceptions/400.jade', {},
                              context_instance=RequestContext(request))


def permission_denied_view(request):
    return render_to_response('exceptions/403.jade', {},
                              context_instance=RequestContext(request))


def page_not_found_view(request):
    return render_to_response('exceptions/404.jade', {},
                              context_instance=RequestContext(request))


def error_view(request):
    return render_to_response('exceptions/500.jade', {},
                              context_instance=RequestContext(request))


class PermissionRequiredMixin:
    permission_required = None

    def check_permission_required(self):
        if self.permission_required:
            if not self.request.user.has_perm(self.permission_required):
                raise PermissionDenied


class BaseDetailView(DetailView, PermissionRequiredMixin):

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        return '{}: {}'.format(verbose_name, self.object).capitalize()

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = self.get_title()

        return context


class BaseSlugDetailView(BaseDetailView):
    slug_url_kwarg = 'slug'

    def get_slug_field(self):
        return "slug_{}".format(self.request.LANGUAGE_CODE)

    def get_object(self, *args, **kwargs):
        try:
            obj = self.model.objects.get_by_slug(self.kwargs['slug'])
        except:
            raise Http404(
                _("No %(verbose_name)s found matching the query") %
                {'verbose_name': self.model._meta.verbose_name}
            )
        return obj

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class BaseCreateView(CreateView, PermissionRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)

        verbose_name = self.model._meta.verbose_name
        context['opts'] = self.model._meta
        context['title'] = _('Create %s') % verbose_name
        context['cancel_url'] = self.get_cancel_url()

        return context

    def get_cancel_url(self):
        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseCreateView, self).dispatch(*args, **kwargs)


class BaseSubModelCreateView(CreateView, PermissionRequiredMixin):
    """
    Create view when the object is nested within a parent object
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseSubModelCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        model_underscore_name = underscore(self.parent_model.__name__)

        obj = get_object_or_404(
            self.parent_model,
            pk=self.kwargs['{}_id'.format(model_underscore_name)]
        )

        self.object = self.model(**{model_underscore_name: obj})

        return super(BaseSubModelCreateView, self).get_form_kwargs()

    def get_context_data(self, **kwargs):
        context = super(BaseSubModelCreateView, self).get_context_data(
            **kwargs
        )
        model_underscore_name = underscore(self.parent_model.__name__)

        obj = get_object_or_404(
            self.parent_model,
            pk=self.kwargs['{}_id'.format(model_underscore_name)]
        )

        context[model_underscore_name] = obj
        context['title'] = _('Create %s') % self.model._meta.verbose_name
        context['cancel_url'] = obj.get_absolute_url()

        return context


class BaseListView(ListView, PermissionRequiredMixin):
    paginate_by = 25
    page_kwarg = 'p'

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.getlist('o')
        if order:
            return order

        return self.ordering

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['clean_query_string'] = clean_query_string(self.request)
        context['q'] = self.request.GET.get('q')
        context['title'] = self.model._meta.verbose_name_plural.capitalize()
        context['ordering'] = self.request.GET.getlist('o')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)


class BaseTemplateView(TemplateView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseTemplateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = self.model._meta

        return context


class BaseUpdateView(UpdateView, PermissionRequiredMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['cancel_url'] = self.object.get_absolute_url()
        context['title'] = _('Update %s') % str(self.object)

        return context


class BaseDeleteView(DeleteView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseDeleteView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = _('Delete %s') % str(self.object)

        return context

    def get_success_url(self):
        model_name = self.model.__name__.lower()
        return reverse('{}_list'.format(model_name))


class BaseRedirectView(RedirectView, PermissionRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseRedirectView, self).dispatch(*args, **kwargs)


class AboutTemplateView(TemplateView):
    template_name = 'about.pug'


class AboutInteriorTemplateView(TemplateView):
    template_name = 'about_interior.pug'
