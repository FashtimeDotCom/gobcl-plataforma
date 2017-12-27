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

from filer.fields.image import FilerImageField
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from cms.utils.i18n import get_current_language

from .managers import CampaignQueryset


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

    objects = CampaignQueryset.as_manager()

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = (
            '-is_featured',
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
            return reverse('campaigns:campaign_detail', args=(self.slug,), )

    def save(self, *args, **kwargs):
        language = get_current_language()
        activate(language=language)
        self.slug = slugify(self.title)
        return super(Campaign, self).save(*args, **kwargs)

    def is_active(self):
        now = timezone.now()
        return (self.activation_datetime <= now and
                self.deactivation_datetime >= now)
