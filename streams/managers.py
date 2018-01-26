from base.managers import TranslatableQuerySet


class StreamQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            is_active=True,
        )


class StreamEventQueryset(TranslatableQuerySet):
    pass
