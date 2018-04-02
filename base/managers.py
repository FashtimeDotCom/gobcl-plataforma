""" This document defines the Base Manager and BaseQuerySet classes"""

# django
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Count
from django.core.exceptions import MultipleObjectsReturned
from parler.managers import TranslatableQuerySet as BaseTranslatableQuerySet

# standard library
import json


class QuerySet(models.query.QuerySet):

    def to_json(self):
        return json.dumps(list(self.values()), cls=DjangoJSONEncoder)

    def find_duplicates(self, *fields):
        duplicates = self.values(*fields).annotate(Count('id'))
        return duplicates.order_by().filter(id__count__gt=1)

    def get_or_none(self, **fields):
        queryset = self
        try:
            return queryset.get(**fields)
        except (self.model.DoesNotExist, MultipleObjectsReturned):
            return None


class TranslatableQuerySet(BaseTranslatableQuerySet, QuerySet):
    pass


class BaseManager(models.Manager):
    """
     This is the base manager, all model should implement it
    """

    def get_queryset(self):
        """
        Returns a new QuerySet object.
        """
        return QuerySet(self.model, using=self._db)

    def to_json(self):
        qs = self.get_queryset()

        return json.dumps(list(qs.values()), cls=DjangoJSONEncoder)

    def find_duplicates(self, *fields):
        qs = self.get_queryset()
        return qs.find_duplicates(*fields)

    def get_or_none(self, **fields):
        try:
            return self.get_queryset().get(**fields)
        except (self.model.DoesNotExist, MultipleObjectsReturned):
            return None


class BaseGovernmentQuerySet(TranslatableQuerySet):

    def by_government_structure(self, government_structure):
        return self.filter(government_structure=government_structure)

    def current_government(self):
        return self.filter(government_structure__current_government=True)
