""" This document defines the Region app managers classes"""
from base.managers import BaseGovernmentQuerySet
from institutions.managers import InstitutionQuerySet
from aldryn_apphooks_config.managers.base import ManagerMixin
from parler.managers import TranslatableManager


class CommuneQuerySet(InstitutionQuerySet):
    def by_government_structure(self, government_structure):
        qs = self
        return qs.filter(region__government_structure=government_structure)

    def with_own_municipality(self):
        return self.filter(has_own_municipality=True)

    def current_government(self):
        return self.filter(
            region__government_structure__current_government=True
        )


class RegionQuerySet(BaseGovernmentQuerySet):
    pass


class RegionManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        return RegionQuerySet(self.model, using=self.db)

    def by_government_structure(self, government_structure):
        return self.get_queryset().by_government_structure(
            government_structure
        )

    def bulk_index(self, boost=1, government_structure=None):
        queryset = self.get_queryset().by_government_structure(
            government_structure
        )

        languages = ('es', 'en')
        for language in languages:
            queryset = queryset.language(language)
            for obj in queryset:
                obj.index_in_elasticsearch(boost)
