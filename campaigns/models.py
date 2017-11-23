# -*- coding: utf-8 -*-
""" Models for the campaigns application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

# models
from base.models import BaseModel
from django.contrib.sites.models import Site
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


from filer.fields.image import FilerImageField


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
    is_featured = models.BooleanField(
        _('is featured'),
        default=False,
    )

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        permissions = (
            ('view_campaign', _('Can view campaign')),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns the canonical URL for the Campaign object """
        return reverse('campaign_detail', args=(self.pk,))

    def save(self, *args, **kwargs):
        if not self.external_url:
            self.create_page()
        return super(Campaign, self).save(*args, **kwargs)

    def create_page(self):

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
            language='es',
            slug=slugify(self.title)
        )
