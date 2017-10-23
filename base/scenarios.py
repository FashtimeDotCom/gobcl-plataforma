import requests

from django.utils import timezone
from django.conf import settings

from base.mockups import Mockup

from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from institutions.models import InstitutionURL


def create_government_structure(date=None):
    m = Mockup()
    if date is None:
        date = timezone.datetime.now()
    return m.create_government_structure(
        publication_date=date,
        current_government=True
    )


def create_ministry(date=None, quantity=10):
    m = Mockup()
    government_structures = GovernmentStructure.objects.filter(
        current_government=True)
    if government_structures.exists():
        government_structure = government_structures.first()
    else:
        government_structure = create_government_structure(date)

    for x in range(quantity):
        minister = m.create_public_servant(
            government_structure=government_structure,
        )
        m.create_ministry(
            minister=minister,
            government_structure=government_structure,
        )


def create_ministries_by_data(date=None):

    # get or create current government structure
    m = Mockup()
    government_structures = GovernmentStructure.objects.filter(
        current_government=True)
    if government_structures.exists():
        government_structure = government_structures.first()
    else:
        government_structure = create_government_structure(date)

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
            minister = m.create_public_servant(
                government_structure=government_structure,
            )

            # get or create ministry by government structure and name
            ministry_obj = Ministry.objects.get_or_create(
                government_structure=government_structure,
                name=name,
                defaults={
                    'description': description,
                    'minister': minister,
                }
            )[0]

            '''
            if rest has "servicios dependientes"
            get or create Institution URL and appends in list
            '''
            services = []
            for service in source.get('servicios_dependientes'):
                url = service.get('url')
                if not url:
                    continue
                url = InstitutionURL.objects.get_or_create(url=url)[0]
                services.append(url)

            # if the list of services has elements, it's added to the ministry
            if services:
                ministry_obj.public_enterprises.add(*services)
