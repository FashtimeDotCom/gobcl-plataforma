# standard library imports
import string
import uuid
import random

from django.utils import timezone

from base.utils import random_string

from government_structures.models import GovernmentStructure
from regions.models import Region
from ministries.models import Ministry
from public_servants.models import PublicServant


class Mockup(object):

    def create_government_structure(self, **kwargs):
        self.set_required_datetime(kwargs, 'publication_date')
        return GovernmentStructure.objects.create(**kwargs)

    def create_public_servant(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return PublicServant.objects.create(**kwargs)

    def create_ministry(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return Ministry.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'government_structure')
        self.set_required_foreign_key(
            kwargs, 'governor', model='public_servant')
        return Region.objects.create(**kwargs)

    #
    def random_email(self):
        return "{}@{}.{}".format(
            self.random_string(length=6),
            self.random_string(length=6),
            self.random_string(length=2)
        )

    def random_hex_int(self, *args, **kwargs):
        val = self.random_int(*args, **kwargs)
        return hex(val)

    def random_int(self, minimum=-100000, maximum=100000):
        return random.randint(minimum, maximum)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)

    def random_string(self, length=6, chars=None):
        return random_string(length=length, chars=chars)

    def random_uuid(self, *args, **kwargs):
        chars = string.digits
        return uuid.UUID(''.join(random.choice(chars) for x in range(32)))

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:

            if default is None:
                data[field] = not not random.randint(0, 1)
            else:
                data[field] = default

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_ip_address(self, data, field, **kwargs):
        if field not in data:
            ip = '{}.{}.{}.{}'.format(
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
            )
            data[field] = ip

    def set_required_rut(self, data, field, length=6):
        if field not in data:
            rut = '{}.{}.{}-{}'.format(
                self.random_int(minimum=1, maximum=99),
                self.random_int(minimum=100, maximum=990),
                self.random_int(minimum=100, maximum=990),
                self.random_string(length=1, chars='k' + string.digits),
            )
            data[field] = rut

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))
