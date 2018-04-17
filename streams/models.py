# -*- coding: utf-8 -*-
""" Models for the streams application. """
# standard library
from urllib.parse import urlparse
from urllib.parse import parse_qs

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from django.core.exceptions import ValidationError

# models
from base.models import BaseModel

from .managers import StreamQueryset
from .managers import StreamEventQueryset


class Stream(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            _('name'),
            max_length=250,
        ),
        description=models.TextField(
            _('description'),
        )
    )
    url = models.URLField(
        _('url'),
        max_length=250,
        blank=True,
        null=True,
    )
    iframe = models.TextField(
        _('iframe'),
        blank=False,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=False,
    )

    objects = StreamQueryset.as_manager()

    class Meta:
        verbose_name = _('stream')
        verbose_name_plural = _('streams')
        permissions = (
            ('view_stream', _('Can view stream')),
        )

    def __str__(self):
        return self.title

    def get_url(self):
        if self.is_youtube():
            url_data = urlparse(self.url)
            query = parse_qs(url_data.query)
            youtube_id = query.get('v')[0]
            url = 'https://www.youtube.com/embed/{}/?autoplay=1'.format(
                youtube_id
            )
            return url

        elif self.is_mediastream():
            url = 'http://mdstrm.com/live-stream/57a498c4d7b86d600e5461cb'
            url += '?jsapi=true&amp;autoplay=true&amp;controls=true&amp;volume=75&amp;player=57f40bb4dc5b9f3075c49cfe&amp;custom.preroll=&amp;custom.overlay='
            return url

        elif self.is_facebook():
            url = 'https://www.facebook.com/plugins/video.php?href={}'.format(
                self.url
            )
            url += '?&width=560&show_text=false&height=315&autoplay=true'
            return url

    def is_youtube(self):
        return 'youtube' in self.url

    def is_mediastream(self):
        return 'mdstrm' in self.url

    def is_facebook(self):
        return 'facebook' in self.url

    def save(self, *args, **kwargs):
        if self.is_active:
            Stream.objects.filter(is_active=True).update(is_active=False)
        return super(Stream, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stream_detail', args=(self.pk,))


class StreamEvent(BaseModel, TranslatableModel):
    stream = models.ForeignKey(
        Stream,
        verbose_name=_('stream'),
        related_name='events',
        null=True,
        on_delete=models.SET_NULL,
    )
    translations = TranslatedFields(
        title=models.CharField(
            _('name'),
            max_length=250,
        ),
        description=models.TextField(
            _('description'),
        )
    )
    date_time = models.DateTimeField(
        _('date time'),
    )

    objects = StreamEventQueryset.as_manager()

    class Meta:
        verbose_name = _('stream event')
        verbose_name_plural = _('stream events')
        ordering = ('-date_time',)

    def __str__(self):
        return self.title
