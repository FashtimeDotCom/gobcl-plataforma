from django.utils.translation import activate

from ministries.models import PublicService
from ministries.models import Ministry


def create_public_service(row, government_structure):

    public_service_list = []

    for cell in row[:3]:
        value = cell.value
        if value == 'Ministerio al que pertenece':
            return
        public_service_list.append(value)

    activate('es')

    ministry = Ministry.objects.translated(
        name__icontains=public_service_list[0].strip()
    ).first()

    if not public_service_list[1] or not ministry:
        return

    data = {
        'name': public_service_list[1],
        'ministry': ministry,
    }

    public_service = PublicService.objects.create(**data)

    public_service.set_current_language('en')

    public_service.name = public_service_list[2]
    public_service.save()
