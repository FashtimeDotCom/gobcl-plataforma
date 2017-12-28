from base.managers import TranslatableQuerySet
from base.managers import BaseManager
from django.utils import timezone


class CampaignQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            activation_datetime__lte=timezone.now(),
            deactivation_datetime__gte=timezone.now(),
        )


class CampaignManager(BaseManager):

    def get_queryset(self):
        """
        Returns a new CampaignQuerySet object.
        """
        return CampaignQueryset(
            self.model,
            using=self._db
        ).select_related('image')

    def active(self):
        return self.get_queryset().active()
