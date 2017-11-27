# -*- coding: utf-8 -*-
""" Models for the campaigns application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# models
from base.models import BaseModel
from django.contrib.sites.models import Site
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


from filer.fields.image import FilerImageField
from gobcl_cms.utils import create_text_plugin
from gobcl_cms.utils import create_picture_plugin

from .managers import CampaignQueryset


class Campaign(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=100,
    )
    image = FilerImageField(
        verbose_name=_('image'),
    )
    external_url = models.URLField(
        _('external url'),
        max_length=200,
        blank=True,
    )
    description = models.TextField(
        _('description'),
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )
    featured_since = models.DateTimeField(
        _('featured since'),
        blank=True,
        null=True,
    )
    featured_until = models.DateTimeField(
        _('featured until'),
        blank=True,
        null=True,
    )
    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
    )

    objects = CampaignQueryset.as_manager()

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        permissions = (
            ('view_campaign', _('Can view campaign')),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        else:
            return self.page.get_absolute_url()

    def save(self, *args, **kwargs):
        if not self.external_url and not self.page:
            self._create_page()
        return super(Campaign, self).save(*args, **kwargs)

    def _create_page(self, language='es'):

        site = Site.objects.get_current()
        page = Page.objects.create(
            site=site,
            template='campaigns/campaign_detail.pug',
        )
        page.in_navigation = False
        page.save()

        Title.objects.create(
            title=self.title,
            page=page,
            language=language,
            slug=slugify(self.title),
            published=self.is_active,
        )

        placeholder = page.placeholders.filter(
                slot='newsblog_article_content'
            ).first()

        create_picture_plugin(
            self.image,
            placeholder,
            language,
            0,
        )

        create_text_plugin(
            self.description,
            placeholder,
            language,
            1,
        )

        self.page = page
