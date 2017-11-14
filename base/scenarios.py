import requests

# django
from django.contrib.sites.models import Site
from django.db.models import F

# mockups
from base.mockups import Mockup
from base.data import regions_data

# models
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Commune
from regions.models import Region


def get_current_government_structure():
    mockup = Mockup()

    return mockup.get_or_create_government_structure(
        current_government=True
    )[0]


def create_presidency():
    m = Mockup()
    government_structure = get_current_government_structure()
    m.create_presidency(government_structure=government_structure)


def create_ministry(datetime=None, quantity=10):
    m = Mockup()
    government_structure = get_current_government_structure()

    for x in range(quantity):
        minister = m.create_public_servant(
            government_structure=government_structure,
        )
        m.create_ministry(
            minister=minister,
            government_structure=government_structure,
        )


def create_cms_pages():
    mockup = Mockup()
    site_id = Site.objects.first().id

    mockup.get_or_create_page(
        reverse_id=u'Noticias',
        template=u'base.jade',
        site_id=site_id,
    )


def load_regions(datetime=None, quantity=10):
    government_structure = get_current_government_structure()

    for region_data in regions_data:
        name = region_data['name']
        region = Region.objects.get_or_create(
            government_structure=government_structure,
            name=name,
        )[0]

        if not region.name_es:
            region.name_es = name

        if not region.name_en:
            region.name_en = name

        region.save()

        for commune_data in region_data['communes']:
            Commune.objects.get_or_create(
                name=commune_data['name'],
                region=region,
            )


def load_data_from_digital_gob_api(ministry_with_minister=False):

    # get or create current government structure
    m = Mockup()
    government_structure = get_current_government_structure()

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
            if not ministry_obj.name_es:
                ministry_obj.name_es = name

            if not ministry_obj.name_en:
                ministry_obj.name_en = name

            ministry_obj.save()

            '''
            If rest has "servicios dependientes"
            get or create PublicService
            '''
            for service in source.get('servicios_dependientes'):
                name = service.get('nombre')
                url = service.get('url', None)

                if not url:
                    continue

                PublicService.objects.get_or_create(
                    name=name,
                    defaults={
                        'url': url,
                        'ministry': ministry_obj,
                    }
                )[0]


def load_base_data():
    load_regions()
    load_data_from_digital_gob_api()
    PublicService.objects.filter(name_es=None).update(name_es=F('name'))
    PublicService.objects.filter(name_en=None).update(name_es=F('name'))
