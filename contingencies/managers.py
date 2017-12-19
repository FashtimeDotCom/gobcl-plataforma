from base.managers import QuerySet


class ContingencyQueryset(QuerySet):

    def active(self):
        return self.filter(
            is_active=True,
        )
