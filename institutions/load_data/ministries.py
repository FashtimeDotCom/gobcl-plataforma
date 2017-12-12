from django.utils.translation import activate

from public_servants.models import PublicServant
from ministries.models import Ministry


def _create_minister(ministry, government_structure):

    twitter = ''
    if ministry[7]:
        twitter = ministry[7].split('@')[1]

    data = {
        'charge': ministry[6],
        'twitter': twitter,
    }

    activate('es')

    public_servant = PublicServant.objects.get_or_create(
        name=ministry[4],
        government_structure=government_structure,
        defaults=data
    )[0]

    public_servant.set_current_language('en')

    public_servant.charge = ministry[5]
    public_servant.save()

    return public_servant


def create_ministry(row, government_structure):

    ministry = []

    for cell in row[:11]:
        value = cell.value
        if value == 'Ministerio':
            return
        ministry.append(value)

    if ministry[0] is None:
        return

    facebook = ''
    if ministry[10]:
        facebook = ministry[10].split('@')[1]

    twitter = ''
    if ministry[9]:
        twitter = ministry[9].split('@')[1]

    minister = _create_minister(ministry, government_structure)

    data = {
        'name': ministry[0],
        'description': ministry[3],
        'url': ministry[8],
        'twitter': twitter,
        'facebook': facebook,
        'minister': minister,
        'government_structure': government_structure,
    }

    activate('es')

    ministry_object = Ministry.objects.create(**data)

    activate('en')

    ministry_object = Ministry.objects.get(pk=ministry_object.pk)

    ministry_object.name = ministry[1]
    ministry_object.save()
