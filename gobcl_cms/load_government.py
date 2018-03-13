from django.utils.translation import activate

from openpyxl import load_workbook

from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from regions.models import Region
from public_servants.models import PublicServant


def create_sub_secretary(row, government_structure):

    sub_secretary = []
    for cell in row[:10]:
        value = cell.value
        if value == 'nombre':
            return
        sub_secretary.append(value)

    if sub_secretary[0] is None:
        return

    ministry = sub_secretary[1]

    activate('es')
    data = {
        'charge': sub_secretary[2],
        'description': sub_secretary[4],
        'email': sub_secretary[6] or '',
        'phone': sub_secretary[7] or '',
        'twitter': sub_secretary[8] or '',
    }

    sub_secretary_obj = PublicServant.objects.get_or_create(
        name=sub_secretary[0],
        government_structure=government_structure,
        defaults=data,
    )[0]

    ministry = Ministry.objects.filter(
        translations__name__icontains=ministry,
        government_structure=government_structure).first()

    ministry.public_servants.add(sub_secretary_obj)
    ministry.save()


def create_governor(row, government_structure):

    governor = []
    for cell in row[:10]:
        value = cell.value
        if value == 'nombre':
            return
        governor.append(value)

    if governor[0] is None:
        return

    region = governor[1]

    activate('es')
    data = {
        'charge': governor[2],
        'description': governor[4],
        'email': governor[6] or '',
        'phone': governor[7] or '',
        'twitter': governor[8] or '',
    }

    governor_obj = PublicServant.objects.get_or_create(
        name=governor[0],
        government_structure=government_structure,
        defaults=data,
    )[0]
    region = Region.objects.filter(
        translations__name__icontains=region,
        government_structure=government_structure).first()

    region.governor = governor_obj
    region.save()


def create_minister(row, government_structure):

    minister = []
    for cell in row[:10]:
        value = cell.value
        if value == 'nombre':
            return
        minister.append(value)

    if minister[0] is None:
        return

    ministry = minister[1]

    activate('es')
    ministry = Ministry.objects.filter(
        translations__name__icontains=ministry,
        government_structure=government_structure).first()

    data = {
        'name': minister[0],
        'charge': minister[2],
        'description': minister[4],
        'email': minister[6],
        'phone': minister[7],
        'twitter': minister[8],
        'ministry': ministry,
    }

    public_servant = PublicServant.objects.create(**data)
    public_servant.set_current_language('en')
    public_servant.charge = minister[3]
    public_servant.description = minister[4]
    public_servant.save()


def load_government(xlsx_file='Cambio_de_mando.xlsx'):
    wb = load_workbook(xlsx_file)

    sheets = {
        'Ministros': None,
        'Servicios públicos': None,
        'Sub secretarios': create_sub_secretary,
        'Intendentes': create_governor,
        'Región': None,
        'Empresas publicas': None,
        'Comunas': None,
    }

    government_structure = GovernmentStructure.objects.get_or_none(
        current_government=True)

    for sheet_name in wb.get_sheet_names():
        sheet = wb.get_sheet_by_name(sheet_name)

        for row in sheet.rows:
            if sheets.get(sheet_name):
                sheets.get(sheet_name)(row, government_structure)
