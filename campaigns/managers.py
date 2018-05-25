from base.managers import TranslatableQuerySet
from base.managers import TranslatableManager
from django.utils import timezone


class CampaignQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            activation_datetime__lte=timezone.now(),
            deactivation_datetime__gte=timezone.now(),
        )


class CampaignManager(TranslatableManager):

    def get_queryset(self):
        """
        Returns a new CampaignQuerySet object.
        """
        queryset = CampaignQueryset(
            self.model,
            using=self._db
        ).select_related('image')

        return queryset

    def active(self):
        return self.get_queryset().active()

    def bulk_index(self, boost=1):
        queryset = self.get_queryset().translated(
            title__isnull=False,
        )
        print()
        print('=' * 30)
        print('Campaign')

        languages = ('es', 'en')
        for language in languages:
            print('Language:', language)
            queryset = queryset.language(language)
            total = queryset.count()
            print('Total:', total)
            value = 1
            for obj in queryset:
                obj.index_in_elasticsearch(boost)
                print(value, 'of', total)
                value += 1
            print('*' * 10)
