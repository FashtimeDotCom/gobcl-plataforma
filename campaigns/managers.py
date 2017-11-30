from django.utils import timezone

from base.managers import QuerySet
from parler.managers import TranslatableQuerySet


class CampaignQueryset(QuerySet, TranslatableQuerySet):

    def featured(self):
        queryset = self
        now = timezone.now()

        queryset = queryset.filter(
            featured_since__gte=now,
            featured_until__lte=now,
        )

        return queryset

    def active(self):
        return self.filter(is_active=True)
