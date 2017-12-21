from base.managers import TranslatableQuerySet
from django.utils import timezone


class CampaignQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            activation_datetime__lte=timezone.now(),
            deactivation_datetime__gte=timezone.now(),
        )
