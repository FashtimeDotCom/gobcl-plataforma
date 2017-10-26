import requests

from django.utils import timezone

from base.mockups import Mockup

from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from ministries.models import PublicService


def create_government_structure(datetime=None):
    m = Mockup()
    if datetime is None:
        datetime = timezone.datetime.now()
    return m.create_government_structure(
        publication_date=datetime,
        current_government=True
    )


def create_ministry(datetime=None, quantity=10):
    m = Mockup()
    government_structures = GovernmentStructure.objects.filter(
        current_government=True)
    if government_structures.exists():
        government_structure = government_structures.first()
    else:
        government_structure = create_government_structure(datetime)

    for x in range(quantity):
        minister = m.create_public_servant(
            government_structure=government_structure,
        )
        m.create_ministry(
            minister=minister,
            government_structure=government_structure,
        )


def load_data_from_digital_gob_api(datetime=None, ministry_with_minister=False):

    # get or create current government structure
    m = Mockup()
    government_structures = GovernmentStructure.objects.filter(
        current_government=True)
    if government_structures.exists():
        government_structure = government_structures.first()
    else:
        government_structure = create_government_structure(datetime)

    # Get ministries from public json
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    url = 'https://apis.digital.gob.cl/misc/instituciones/_search?size=1000'
    ministries = requests.get(url, headers=headers)
    ministries = ministries.json()['hits']['hits']

    for ministry in ministries:
        source = ministry['_source']
        name = source['nombre']

        # see if name starts with "ministerio"
        if name.lower().startswith('ministerio'):
            description = source.get('mision', '')
            defaults = {'description': description}

            if ministry_with_minister:

                # create a minister dummy by ministry
                minister = m.create_public_servant(
                    government_structure=government_structure,
                )
                defaults['minister'] = minister

            # get or create ministry by government structure and name
            ministry_obj = Ministry.objects.get_or_create(
                government_structure=government_structure,
                name=name,
                defaults=defaults,
            )[0]

            '''
            If rest has "servicios dependientes"
            get or create PublicService
            '''
            for service in source.get('servicios_dependientes'):
                name = service.get('nombre')
                url = service.get('url', None)
                PublicService.objects.get_or_create(
                    name=name,
                    defaults={
                        'url': url,
                        'ministry': ministry_obj,
                    }
                )[0]
