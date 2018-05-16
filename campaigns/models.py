# -*- coding: utf-8 -*-
""" Models for the campaigns application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from cms.models.fields import PlaceholderField
from base.enums import ThumbnailCropChoices

from filer.fields.image import FilerImageField
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from cms.utils.i18n import get_current_language

# elasticsearch
from searches.elasticsearch.documents import SearchIndex

# managers
from .managers import CampaignManager

# utils
from base.utils import remove_tags


def default_end_datetime():
    return timezone.now() + timezone.timedelta(30)


class Campaign(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=255,
            unique=True,
        ),
        slug=models.SlugField(
            _('slug'),
            blank=True,
            max_length=255,
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
    activation_datetime = models.DateTimeField(
        _('activation datetime`'),
        default=timezone.now,
        help_text=_("The date this campaign will be activated"),
    )
    deactivation_datetime = models.DateTimeField(
        _('deactivation datetime`'),
        default=default_end_datetime,
        help_text=_("The date this campaign will be deactivated"),
    )
    is_featured = models.BooleanField(
        _('is featured'),
        default=False,
    )
    importance = models.PositiveIntegerField(
        _('importance'),
        default=0,
    )
    image_crop_when_single = models.CharField(
        _('image crop when single'),
        help_text=_('crop orientation for size: 1080x600'),
        max_length=255,
        choices=ThumbnailCropChoices.choices,
        default=ThumbnailCropChoices.MIDDLE_CENTER,
    )
    image_crop_when_on_pair = models.CharField(
        _('image crop when on pair'),
        help_text=_('crop orientation for size: 1072x240'),
        max_length=255,
        choices=ThumbnailCropChoices.choices,
        default=ThumbnailCropChoices.MIDDLE_CENTER,
    )
    image_crop_when_on_trio = models.CharField(
        _('image crop when on trio'),
        help_text=_('crop orientation for size: 700x240'),
        max_length=255,
        choices=ThumbnailCropChoices.choices,
        default=ThumbnailCropChoices.MIDDLE_CENTER,
    )
    image_crop_when_small = models.CharField(
        _('image crop when small'),
        help_text=_('crop orientation for size: 164x90'),
        max_length=255,
        choices=ThumbnailCropChoices.choices,
        default=ThumbnailCropChoices.MIDDLE_CENTER,
    )
    header_content = PlaceholderField(
        'campaign header',
        on_delete=models.SET_NULL,
        related_name='campaigns_as_header',
    )
    content = PlaceholderField(
        'campaign content',
        on_delete=models.SET_NULL,
        related_name='campaigns',
    )

    objects = CampaignManager()

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = (
            '-is_featured',
            'importance',
        )
        permissions = (
            ('view_campaign', _('Can view campaign')),
        )

    @classmethod
    def reorder_importance(cls):
        '''
        Take all campaings and change importance value orderly
        '''
        campaings = cls.objects.active()
        importance = 0
        for campaign in campaings:
            campaign.update(importance=importance)
            importance += 1

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.external_url:
            return self.external_url
        else:
            return reverse('campaigns:campaign_detail', args=(self.slug,), )

    def save(self, *args, **kwargs):
        if not self.importance:
            Campaign.reorder_importance()

        language = get_current_language()
        activate(language=language)
        self.slug = slugify(self.title)

        return_value = super(Campaign, self).save(*args, **kwargs)

        self.deindex_in_elasticsearch()
        if self.is_active():
            self.index_in_elasticsearch(1)

        return return_value

    def is_active(self):
        now = timezone.now()
        return (self.activation_datetime <= now and
                self.deactivation_datetime >= now)

    def get_elasticsearch_kwargs(self):
        kwargs = super(Campaign, self).get_elasticsearch_kwargs()
        if hasattr(self, 'title'):
            kwargs['detail'] = self.title

        return kwargs
