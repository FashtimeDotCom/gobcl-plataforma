# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library

# external library

# django
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
from django.views.defaults import bad_request
from django.views.defaults import permission_denied
from django.views.defaults import page_not_found
from django.views.defaults import server_error

# utils
from base.view_utils import clean_query_string
from base.view_utils import get_home_campaigns
from inflection import underscore
from base.utils import get_or_set_cache

# models
from articles.models import Article
from gobcl_cms.models import HeaderImage
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Region
from streams.models import Stream


class IndexTemplateView(TemplateView):
    template_name = 'index.pug'

    def get_context_data(self, **kwargs):
        """ view that renders a default home"""

        articles = Article.objects.published().order_by('-publishing_date')[:4]

        stream = Stream.objects.active().first()
        header_image = HeaderImage.objects.active().order_by('?').first()

        gov_structure = self.request.government_structure

        context = {
            'procedures_and_benefits': None,
            'header_image': header_image,
            'articles': articles,
            'stream': stream,
            'ministries_count': get_or_set_cache(
                'ministries_count',
                Ministry.objects.by_government_structure(gov_structure).count
            ),
            'public_services_count': get_or_set_cache(
                'public_services_count',
                PublicService.objects.by_government_structure(
                    gov_structure
                ).count
            ),
            'regions_count': get_or_set_cache(
                'regions_count',
                Region.objects.by_government_structure(gov_structure).count
            ),
        }

        context.update(get_home_campaigns(self.request))
        return context


def bad_request_view(request, exception, template=None):
    return bad_request(request, exception, 'exceptions/400.pug')


def permission_denied_view(request, exception, template=None):
    return permission_denied(request, exception, 'exceptions/403.pug')


def page_not_found_view(request, exception, template=None):
    return page_not_found(request, exception, 'exceptions/404.pug')


def server_error_view(request, template=None):
    return server_error(request, 'exceptions/500.pug')


class PermissionRequiredMixin:
    permission_required = None

    def check_permission_required(self):
        if self.permission_required:
            if not self.request.user.has_perm(self.permission_required):
                raise PermissionDenied


class BaseDetailView(DetailView, PermissionRequiredMixin):

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        obj = self.object
        return '{}: {}'.format(verbose_name, obj).capitalize()

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
        except self.model.DoesNotExist:
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
            translations__slug=self.kwargs[
                '{}_slug'.format(model_underscore_name)
            ]
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
            translations__slug=self.kwargs[
                '{}_slug'.format(model_underscore_name)
            ]
        )

        context[model_underscore_name] = obj
        context['title'] = _('Create %s') % self.model._meta.verbose_name
        context['cancel_url'] = obj.get_absolute_url()

        return context


class BaseListView(ListView, PermissionRequiredMixin):
    paginate_by = 25
    page_kwarg = 'p'
    ignore_kwargs_on_filter = ('q', page_kwarg, 'o')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['clean_query_string'] = clean_query_string(self.request)
        context['q'] = self.request.GET.get('q')
        context['title'] = self.model._meta.verbose_name_plural.capitalize()
        context['ordering'] = self.request.GET.getlist('o')
        return context

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.getlist('o')
        if order:
            return order

        return self.ordering

    def get_queryset(self):
        """
        return the queryset to use on the list and filter by what comes on the
        query string
        """
        queryset = super(BaseListView, self).get_queryset()

        # obtain non ignored kwargs for the filter method
        items = self.request.GET.items()
        params = dict(
            (k, v) for k, v in items if k not in self.ignore_kwargs_on_filter
        )

        # filter
        for key, value in params.items():
            try:
                queryset = queryset.filter(**{key: value})
            except FieldError:
                pass
        return queryset


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
