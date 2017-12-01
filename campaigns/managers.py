from parler.managers import TranslatableQuerySet
from base.managers import QuerySet


class CampaignQueryset(QuerySet, TranslatableQuerySet):

    def active(self):
        return self.filter(is_active=True)
