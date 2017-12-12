from django.utils.translation import activate

from public_enterprises.models import PublicEnterprise
from ministries.models import Ministry


def create_public_enterprise(row, government_structure):

    public_enterprise = []

    for cell in row[:5]:
        value = cell.value
        if value and value.startswith('Nombres de personas jurídicas'):
            return
        public_enterprise.append(value)

    if public_enterprise[0] is None:
        return

    data = {
        'name': public_enterprise[1],
        'url': public_enterprise[4],
        'government_structure': government_structure,
    }

    activate('es')

    public_enterprise_obj = PublicEnterprise.objects.create(**data)

    ministry = Ministry.objects.translated(
            name__icontains=public_enterprise[3]
        ).first()

    if ministry:
        public_enterprise_obj.ministries.add(ministry)

    activate('en')

    public_enterprise_obj = PublicEnterprise.objects.get(
        pk=public_enterprise_obj.pk)

    public_enterprise_obj.name = public_enterprise[0]
    public_enterprise_obj.save()
