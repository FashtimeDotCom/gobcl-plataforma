from parler.managers import TranslatableQuerySet
from base.managers import QuerySet
from django.utils import timezone


class CampaignQueryset(QuerySet, TranslatableQuerySet):

    def active(self):
        return self.filter(
            activation_datetime__lte=timezone.now(),
            deactivation_datetime__gte=timezone.now(),
        )
