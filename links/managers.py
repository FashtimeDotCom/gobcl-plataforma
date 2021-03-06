from base.managers import BaseGovernmentQuerySet
from aldryn_apphooks_config.managers.base import ManagerMixin
from parler.managers import TranslatableManager


class FooterLinkQueryset(BaseGovernmentQuerySet):
    pass


class FooterLinkManager(ManagerMixin, TranslatableManager):
    def get_queryset(self):
        return FooterLinkQueryset(self.model, using=self.db)

    def by_government_structure(self, government_structure):
        return self.get_queryset().by_government_structure(
            government_structure)

    def bulk_index(self, boost=1, government_structure=None):
        queryset = self.get_queryset().by_government_structure(
            government_structure
        )

        print()
        print('=' * 30)
        print('Footer links')

        total = queryset.count()
        print('Total:', total)
        value = 1

        for obj in queryset:
            obj.index_in_elasticsearch(boost)
            print(value, 'of', total)
            value += 1
