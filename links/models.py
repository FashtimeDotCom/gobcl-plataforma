# -*- coding: utf-8 -*-
""" Models for the links application. """
# standard library

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseGovernmentStructureModel

# elasticsearch
from searches.elasticsearch.documents import SearchIndex

# managers
from .managers import FooterLinkManager


class FooterLink(BaseGovernmentStructureModel):
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    order = models.PositiveSmallIntegerField(
        _('order'),
        default=0,
    )

    objects = FooterLinkManager()

    class Meta:
        verbose_name = _('footer link')
        verbose_name_plural = _('footer links')
        ordering = ('order',)
        permissions = (
            ('view_link', _('Can view link')),
        )

    def get_absolute_url(self):
        return self.url

    def _sum_order(self):
        '''
        When add a FooterLink object, order
        field change to footer links + 1
        '''
        links = FooterLink.objects.count()
        self.order = links + 1

    @classmethod
    def reorder_order(cls):
        '''
        Take all footer links and change order value
        '''
        links = cls.objects.all()
        order = 0
        for link in links:
            link.order = order
            link.save()
            order += 1

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self._sum_order()
        return super(FooterLink, self).save(*args, **kwargs)

    def index_in_elasticsearch(self, boost):
        doc = SearchIndex(
            name=self.name,
            language_code='ALL',
            url=self.get_absolute_url(),
            detail=self.url,
            boost=boost
        )
        doc.save()
