""" This document defines the Institution app managers classes"""

from base.managers import BaseGovernmentQuerySet
from django.db.models import Q


class InstitutionQuerySet(BaseGovernmentQuerySet):
    def get_by_slug(self, slug):
        return self.get(
            Q(slug_en=slug) |
            Q(slug_es=slug)
        )
