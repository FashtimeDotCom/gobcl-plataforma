from base.managers import TranslatableQuerySet


class HeaderImageQueryset(TranslatableQuerySet):

    def active(self):
        return self.filter(
            is_active=True,
        )
