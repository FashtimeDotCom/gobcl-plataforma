from openpyxl import load_workbook

from ministries.models import Ministry
from government_structures.models import GovernmentStructure
from public_servants.models import PublicServant
from public_enterprises.models import PublicEnterprise


def _create_minister(ministry, government_structure):

    twitter = ''
    if ministry[7]:
        twitter = ministry[7].split('@')[1]

    data = {
        'name': ministry[4],
        'charge': ministry[6],
        'charge_en': ministry[5],
        'twitter': twitter,
        'government_structure': government_structure,
    }
    return PublicServant.objects.create(**data)


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
        'name_en': ministry[1],
        'name_es': ministry[2],
        'description': ministry[3],
        'url': ministry[8],
        'twitter': twitter,
        'facebook': facebook,
        'minister': minister,
        'government_structure': government_structure,
    }

    Ministry.objects.create(**data)


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

    PublicEnterprise.objects.create(**data)


def load_data_from_xlsx():
    wb = load_workbook('gobcl.xlsx')

    sheets = {
        'Ministerios': None,
        'Subsecretarios': None,
        'Intendencias': None,
        'Servicios Públicos': None,
        'Empresas Públicas': create_public_enterprise,
        'Campañas': None,
        'Acerca de Chile': None,
        'Nuestro país': None,
        'Presidencia': None,
    }

    government_structure = GovernmentStructure.objects.get_or_none(
            current_government=True)

    for sheet_name in wb.get_sheet_names():
        sheet = wb.get_sheet_by_name(sheet_name)

        for row in sheet.rows:
            if sheets.get(sheet_name):
                sheets.get(sheet_name)(row, government_structure)
