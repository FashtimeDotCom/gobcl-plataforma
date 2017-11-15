# -*- coding: utf-8 -*-
""" Models for the ministries application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from institutions.models import Institution
from ministries.managers import PublicServiceQuerySet


class Ministry(Institution):
    # foreign keys
    minister = models.ForeignKey(
        'public_servants.PublicServant',
        verbose_name=_('minister'),
        null=True,
        on_delete=models.SET_NULL,
    )
    public_servants = models.ManyToManyField(
        'public_servants.PublicServant',
        verbose_name=_('public servants'),
        related_name='ministries',
    )

    # required fields
    procedures_and_benefits = models.URLField(
        _('procedures and benefits'),
        max_length=200,
        blank=True,
    )
    importance = models.PositiveIntegerField(
        _('importance'),
        default=0,
    )

    class Meta:
        ordering = ('importance',)
        verbose_name = _('ministry')
        verbose_name_plural = _('ministries')
        unique_together = ('name', 'government_structure')

    def __str__(self):
        return self.name

    def _sum_importance(self):
        '''
        When add a Ministry object, importance
        field change to total ministries + 1
        '''
        ministries = Ministry.objects.count()
        self.importance = ministries + 1

    @classmethod
    def reorder_importance(cls):
        '''
        Take all ministries and change importance value orderly
        '''
        ministries = cls.objects.all()
        importance = 0
        for ministry in ministries:
            ministry.importance = importance
            ministry.save()
            importance += 1

    def get_absolute_url(self):
        """ Returns the canonical URL for the public_servant object """
        return reverse('ministry_detail', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.pk:
            self._sum_importance()
        return super(Ministry, self).save(*args, **kwargs)


class PublicService(BaseModel):
    ministry = models.ForeignKey(
        Ministry,
        verbose_name=_('ministry'),
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )

    objects = PublicServiceQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('public service')
        verbose_name_plural = _('public services')
        unique_together = ('name', 'ministry')
