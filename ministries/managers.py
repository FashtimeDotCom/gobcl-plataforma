""" This document defines the Ministries app managers classes"""
from institutions.managers import InstitutionQuerySet
from base.managers import BaseGovernmentQuerySet
from aldryn_apphooks_config.managers.base import ManagerMixin
from parler.managers import TranslatableManager


class PublicServiceQuerySet(InstitutionQuerySet):
    def by_government_structure(self, government_structure):
        qs = self
        return qs.filter(ministry__government_structure=government_structure)

    def current_government(self):
        return self.filter(
            ministry__government_structure__current_government=True
        )


class PublicServiceManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        return PublicServiceQuerySet(self.model, using=self.db)

    def by_government_structure(self, government_structure):
        return self.get_queryset().by_government_structure(government_structure)

    def bulk_index(self, boost=1, government_structure=None):
        queryset = self.get_queryset().translated(
            name__isnull=False,
        ).by_government_structure(
            government_structure
        )

        print()
        print('=' * 30)
        print('Public services')

        languages = ('es', 'en')
        for language in languages:
            queryset = queryset.language(language)

            print('Language:', language)
            total = queryset.count()
            print('Total:', total)
            value = 1

            for obj in queryset:
                obj.index_in_elasticsearch(boost)
                print(value, 'of', total)
                value += 1
            print('*' * 10)


class MinistryQueryset(BaseGovernmentQuerySet):
    pass


class MinistryManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        return MinistryQueryset(self.model, using=self.db)

    def by_government_structure(self, government_structure):
        return self.get_queryset().by_government_structure(
            government_structure)

    def bulk_index(self, boost=1, government_structure=None):
        queryset = self.get_queryset().filter(
            government_structure=government_structure
        ).translated(
            name__isnull=False,
        )

        print()
        print('=' * 30)
        print('Ministries')

        languages = ('es', 'en')
        for language in languages:
            queryset = queryset.language(language)

            print('Language:', language)
            total = queryset.count()
            print('Total:', total)
            value = 1

            for obj in queryset:
                obj.index_in_elasticsearch(boost)
                print(value, 'of', total)
                value += 1
            print('*' * 10)
