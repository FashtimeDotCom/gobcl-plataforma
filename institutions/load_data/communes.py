from django.utils.translation import activate

from regions.models import Commune
from regions.models import Region


def create_commune(row, government_structure):

    commune_list = []

    for cell in row[:11]:
        value = cell.value
        if value == 'N':
            return
        commune_list.append(value)

    if commune_list[0] is None:
        return

    activate('es')

    print(row[5])
    print('*' * 10)
    region = Region.objects.translated(
        name__icontains=commune_list[5]
    ).first()

    data = {
        'region': region,
        'name': commune_list[3],
        'url': commune_list[1],
    }

    Commune.objects.create(**data)
