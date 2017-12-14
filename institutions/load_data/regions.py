from django.utils.translation import activate

from regions.models import Region
from public_servants.models import PublicServant


def _create_governor(region, government_structure):

    twitter = ''
    if region[9]:
        twitter = region[9].split('/')[-1]

    data = {
        'charge': region[6],
        'twitter': twitter,
    }

    activate('es')

    public_servant = PublicServant.objects.get_or_create(
        name=region[4] or '',
        government_structure=government_structure,
        defaults=data
    )[0]

    public_servant.set_current_language('en')

    public_servant.charge = region[5]
    public_servant.save()

    return public_servant


def create_region(row, government_structure):

    region = []

    for cell in row[:10]:
        value = cell.value
        if value == 'Región':
            return
        region.append(value)

    if region[0] is None:
        return

    twitter = ''
    if region[7]:
        twitter = region[7].split('@')[1]

    governor = _create_governor(region, government_structure)

    data = {
        'name': region[2],
        'description': region[3] or '',
        'twitter': twitter,
        'url': region[8] or '',
        'governor': governor,
        'government_structure': government_structure,
    }

    activate('es')

    region_obj = Region.objects.create(**data)

    region_obj.set_current_language('en')

    region_obj.name = region[1]
    region_obj.description = ''
    region_obj.save()
