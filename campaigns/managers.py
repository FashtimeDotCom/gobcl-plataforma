from base.managers import QuerySet


class CampaignQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)
