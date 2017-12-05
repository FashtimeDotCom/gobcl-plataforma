# -*- coding: utf-8 -*-
""" Models for the campaigns application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.translation import activate

# models
from base.models import BaseModel
from django.contrib.sites.models import Site
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


from filer.fields.image import FilerImageField
from gobcl_cms.utils import create_text_plugin
from gobcl_cms.utils import create_picture_plugin
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from cms.utils.i18n import get_current_language

from .managers import CampaignQueryset


class Campaign(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=100,
        ),
        description=models.TextField(
            _('description'),
        ),
    )
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    external_url = models.URLField(
        _('external url'),
        max_length=200,
        blank=True,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )
    is_featured = models.BooleanField(
        _('is featured'),
        default=False,
    )
    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    exclude_on_on_delete_test = ('page',)

    objects = CampaignQueryset.as_manager()

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = (
            'is_featured',
        )
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
        language = get_current_language()
        activate(language=language)
        if not self.external_url and not self.page:
            self._create_page(language=language)
        return super(Campaign, self).save(*args, **kwargs)

    def _create_page(self, language='es'):
        '''
        Create CMS page when create
        Campaign without external url
        '''

        activate(language)

        # Create CMS page
        site = Site.objects.get_current()
        page = Page.objects.create(
            site=site,
            template='campaigns/campaign_detail.pug',
        )
        page.in_navigation = False
        page.save()

        # Create Title depends language
        Title.objects.create(
            title=self.title,
            page=page,
            language=language,
            slug=slugify(self.title),
            published=self.is_active,
        )

        # get placeholder content
        placeholder = page.placeholders.filter(
                slot='campaign_content'
            ).first()

        if self.image_id:
            # Create picture plugin by CMS Page
            create_picture_plugin(
                self.image,
                placeholder,
                language,
                0,
            )

        # Create text plugin by CMS Page
        create_text_plugin(
            self.description,
            placeholder,
            language,
            1,
        )

        # associated page to campaign
        self.page = page
        if self.is_active:
            page.publish(language)
