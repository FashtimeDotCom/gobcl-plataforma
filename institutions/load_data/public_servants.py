from django.utils.translation import activate

from public_servants.models import PublicServant


def create_public_servant(row, government_structure):

    public_servant = []

    for cell in row[:6]:
        value = cell.value
        if value == 'Subsecretarios':
            return
        public_servant.append(value)

    twitter = public_servant[4]
    if twitter and twitter != '-':
        twitter = public_servant[4].split('/')[-1]
    else:
        twitter = ''

    name = public_servant[3] or ''

    data = {
        'charge': public_servant[1],
        'twitter': twitter,
    }

    activate('es')

    public_servant_obj = PublicServant.objects.get_or_create(
        name=name,
        government_structure=government_structure,
        defaults=data
    )[0]

    public_servant_obj.set_current_language('en')

    public_servant_obj.charge = public_servant[2]
    public_servant_obj.save()
