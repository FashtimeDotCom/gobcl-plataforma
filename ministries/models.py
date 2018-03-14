# -*- coding: utf-8 -*-
""" Models for the ministries application. """
# standard library

# django
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

# cms
from cms.utils.i18n import get_current_language

# parler
from parler.models import TranslatableModel
from parler.models import TranslatedFields

# models
from base.models import BaseModel
from institutions.models import Institution
from ministries.managers import PublicServiceQuerySet
from institutions.models import institution_translations


class Ministry(Institution):
    translations = institution_translations

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
        blank=True,
    )

    # required fields
    procedures_and_benefits = models.URLField(
        _('procedures and benefits'),
        max_length=200,
        blank=True,
    )
    twitter = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    facebook = models.CharField(
        max_length=100,
        null=True,
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

    def __str__(self):
        return self.name

    def _sum_importance(self):
        '''
        When add a Ministry object, importance
        field change to total ministries + 1
        '''
        ministries = Ministry.objects.count()
        self.importance = ministries + 1

    def clean(self):
        super(Ministry, self).clean()

        language = get_current_language()
        activate(language)

        ministry = Ministry.objects.active_translations(
            name=self.name
        ).filter(
            government_structure=self.government_structure,
        )

        if self.pk:
            ministry = ministry.exclude(pk=self.pk)

        if ministry.first():
            message = _(
                "ministries's name and government structure, are not unique."
            )
            raise ValidationError(
                {'government_structure': message}
            )

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self._sum_importance()
        return super(Ministry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ Returns the canonical URL for the ministry object """
        return reverse('ministry_detail', args=(self.slug,))


class PublicService(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=255,
        ),
    )

    ministry = models.ForeignKey(
        Ministry,
        verbose_name=_('ministry'),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        blank=True,
        null=True,
    )

    importance = models.PositiveIntegerField(
        _('importance'),
        default=0,
    )

    objects = PublicServiceQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        ordering = ('importance',)
        verbose_name = _('public service')
        verbose_name_plural = _('public services')
