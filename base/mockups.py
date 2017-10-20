from django.utils import timezone

from government_structures.models import GovernmentStructure
from regions.models import Region
from public_servants.models import PublicServant


class Mockup(object):

    def create_government_structure(self, **kwargs):
        self.set_required_date(kwargs, 'publication_date')
        return GovernmentStructure.objects.create(**kwargs)

    def create_public_servant(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'government_structure')
        return PublicServant.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'government_structure')
        self.set_required_foreign_key(
            kwargs, 'governor', model='public_servant')
        return Region.objects.create(**kwargs)

    #
    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()
