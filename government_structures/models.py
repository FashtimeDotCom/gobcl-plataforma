# -*- coding: utf-8 -*-
""" Models for the government_structures application. """
# standard library
import copy

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


class GovernmentStructure(BaseModel):
    publication_date = models.DateTimeField(
        _('publication date'),
        unique=True,
    )
    current_government = models.BooleanField(
        _('current government'),
        default=False,
    )

    class Meta:
        verbose_name = _('government structure')
        verbose_name_plural = _('government structures')
        permissions = (
            ('view_government_structure', _('Can view government structures')),
        )

    def __str__(self):
        return '{}'.format(self.publication_date)

    def save(self, **kwargs):
        # Make sure the default government are unique
        if self.current_government:
            GovernmentStructure.objects.filter(
                current_government=True,
            ).update(
                current_government=False,
            )
        super(GovernmentStructure, self).save(**kwargs)

    @classmethod
    def get_government(cls, date=None):
        if not date:
            return cls.objects.get_or_none(current_government=True)
        now = timezone.datetime.now()

    def duplicate(self, date):
        government_structures = GovernmentStructure.objects.filter(
            publication_date=date)
        if government_structures.exists():
            return

        government_structure = copy.copy(self)
        government_structure.id = None
        government_structure.publication_date = date
        government_structure.save()

        for field in government_structure._meta.fields_map.values():
            model = field.related_model
            objects = model.objects.filter(government_structure=self)
            for obj in objects:
                new_obj = copy.copy(obj)
                new_obj.id = None
                new_obj.government_structure = government_structure
                new_obj.save()
