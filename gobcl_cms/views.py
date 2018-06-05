# -*- coding: utf-8 -*-
""" Views for the Article application. """
# standard library

# django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.contrib.redirects.models import Redirect
from django.views.generic import TemplateView

# base
from django.views.generic import FormView
from django.shortcuts import get_object_or_404

# utils
from base.utils import get_or_set_cache
from base.view_utils import get_home_campaigns

# models
from aldryn_newsblog.models import NewsBlogConfig
from articles.models import Article
from gobcl_cms.models import HeaderImage
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Region
from streams.models import Stream

# forms
from .forms import ArticleForm

# newsblog
from aldryn_newsblog.views import ArticleList


def get_queryset(self):
    qs = super(ArticleList, self).get_queryset()
    # exclude featured articles from queryset, to allow featured article
    # plugin on the list view page without duplicate entries in page qs.

    # if not self.config:
    #     self.namespace, self.config = get_app_instance(self.request)

    if not self.config:
        self.config = NewsBlogConfig.objects.first()

    exclude_count = self.config.exclude_featured

    if exclude_count:
        featured_qs = Article.objects.all().filter(is_featured=True)
        if not self.edit_mode:
            featured_qs = featured_qs.published()
        exclude_featured = featured_qs[:exclude_count].values_list('pk')
        qs = qs.exclude(pk__in=exclude_featured)

    qs = qs.filter(
        translations__language_code=self.request.LANGUAGE_CODE
    )

    return qs


ArticleList.get_queryset = get_queryset
ArticleList.page_kwarg = 'p'


class ArticleRelatedUpdateView(PermissionRequiredMixin, FormView):
    form_class = ArticleForm
    template_name = 'articles/article_update.pug'
    permission_required = ('articles.change_article',)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        # add article object
        self.article = get_object_or_404(Article, pk=kwargs['pk'])

        return super(
            ArticleRelatedUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):

        # send article object to form class
        kwargs = super().get_form_kwargs()
        kwargs.update({'article': self.article})

        return kwargs

    def get_initial(self):
        initial = super(ArticleRelatedUpdateView, self).get_initial()

        # get initial data from article object
        self.initial_list = list(
            self.article.related.translated().values_list('pk', flat=True))

        # Update initial data
        initial.update({
            'related': self.initial_list
        })

        return initial

    def get_context_data(self, **kwargs):
        context = super(ArticleRelatedUpdateView, self).get_context_data(
            **kwargs
        )

        # send article object to template
        context['article'] = self.article

        return context

    def form_valid(self, form):

        # get related id from POST data
        related_id = self.request.POST.getlist('related')

        # remove old related news
        self.article.related.remove(
            *self.initial_list
        )

        # add related news from POST data
        self.article.related.add(*related_id)

        return super(ArticleRelatedUpdateView, self).form_valid(form)

    def get_success_url(self):

        # Go to article detail
        return self.article.get_absolute_url()


class ArticleRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['article_id'])
        if self.request.LANGUAGE_CODE == 'en':
            return '/en/news/{}/'.format(article.slug)
        return article.get_absolute_url(self.request.LANGUAGE_CODE)


class ArticleDateRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs['slug']
        has_slash = '/'

        if 'ministra-blanco-destaco-que-congreso-aprobara-en-tramite-' in slug:
            has_slash = ''

        slug = '/{}{}'.format(
            slug,
            has_slash
        )
        r = get_object_or_404(Redirect, old_path=slug)
        return r.new_path


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
