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

        languages = ('es', 'en')
        for language in languages:
            queryset = queryset.language(language)
            for obj in queryset:
                obj.index_in_elasticsearch(boost)

    def update_elasticsearch_documents(self):
        languages = ('es', 'en')
        for language in languages:
            queryset = self.language(language).filter(
                translations__title__isnull=False
            )
            for campaign in queryset:
                # Check if it's indexed
                doc = campaign.get_elasticsearch_doc()

                # Campaign is not indexed and should be indexed
                if doc is None and campaign.is_active():
                    campaign.index_in_elasticsearch()

                # Campaign is indexed and should be deindexed
                elif doc is not None and not campaign.is_active():
                    campaign.deindex_in_elasticsearch()
