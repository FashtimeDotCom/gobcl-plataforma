# -*- coding: utf-8 -*-
""" Models for the governments application. """
# standard library
import copy

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# models
from base.models import BaseModel


class Government(BaseModel):
    publication_date = models.DateField(
        _('publication date'),
        unique=True,
    )
    current_government = models.BooleanField(
        _('current government'),
        default=False,
    )

    class Meta:
        verbose_name = _('government')
        verbose_name_plural = _('governments')
        permissions = (
            ('view_government', _('Can view governments')),
        )

    def __str__(self):
        return '{}'.format(self.publication_date)

    def save(self, **kwargs):
        # Make sure the default government are unique
        if self.current_government:
            Government.objects.filter(
                current_government=True,
            ).update(
                current_government=False,
            )
        super(Government, self).save(**kwargs)

    @classmethod
    def get_government(cls, date=None):
        if not date:
            return cls.objects.get_or_none(current_government=True)
        now = timezone.datetime.now()

    def duplicate(self, date):
        governments = Government.objects.filter(publication_date=date)
        if governments.exists():
            return

        government = copy.copy(self)
        government.id = None
        government.publication_date = date
        government.save()

        for field in government._meta.fields_map.values():
            model = field.related_model
            objects = model.objects.filter(government=self)
            for obj in objects:
                new_obj = copy.copy(obj)
                new_obj.id = None
                new_obj.government = government
                new_obj.save()
