from base.managers import BaseGovernmentQuerySet
from aldryn_apphooks_config.managers.base import ManagerMixin
from parler.managers import TranslatableManager


class PublicEnterpriseQueryset(BaseGovernmentQuerySet):
    pass


class PublicEnterpriseManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        return PublicEnterpriseQueryset(self.model, using=self.db)

    def by_government_structure(self, government_structure):
        return self.get_queryset().by_government_structure(government_structure)

    def bulk_index(self, government_structure=None):
        queryset = self.get_queryset().by_government_structure(
            government_structure
        )

        languages = ('es', 'en')
        for language in languages:
            queryset = queryset.language(language)
            for obj in queryset:
                obj.index_in_elasticsearch()
