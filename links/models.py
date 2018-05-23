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
        if self.pk is None:
            self._sum_order()

        return_value = super(FooterLink, self).save(*args, **kwargs)

        self.reindex_in_elasticsearch()

        return return_value

    def get_elasticsearch_kwargs(self):
        kwargs = super(FooterLink, self).get_elasticsearch_kwargs()
        kwargs['detail'] = self.get_absolute_url()

        return kwargs
