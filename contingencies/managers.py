from base.managers import TranslatableQuerySet


class ContingencyQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            is_active=True,
        )


class ContingencyEventQueryset(TranslatableQuerySet):
    pass


class ContingencyInformationQueryset(TranslatableQuerySet):
    pass
