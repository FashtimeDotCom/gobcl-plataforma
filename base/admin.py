from django.contrib.auth.models import Permission


def permission__str__(self):
        return self.name


Permission.__str__ = permission__str__
