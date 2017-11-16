import requests
import json

# django
from django.contrib.sites.models import Site
from django.db.models import F
from django.conf import settings
from django.utils.translation import activate

# mockups
from base.mockups import Mockup
from base.data import regions_data

# models
from ministries.models import Ministry
from ministries.models import PublicService
from regions.models import Commune
from regions.models import Region
from aldryn_newsblog.models import Article
from users.models import User
from aldryn_people.models import Person
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from djangocms_text_ckeditor.models import Text
from cmsplugin_filer_image.models import FilerImage


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
    PublicService.objects.filter(name=None).delete()

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

                public_service = PublicService.objects.get_or_create(
                    name=name.strip(),
                    ministry=ministry_obj,
                    defaults={
                        'name_es': name.strip(),
                        'url': url,
                    }
                )[0]

                if not public_service.name_en:
                    public_service.name_en = name

                public_service.save()


def load_base_data():
    load_regions()
    load_data_from_digital_gob_api()
    PublicService.objects.filter(name_es=None).update(name_es=F('name'))
    PublicService.objects.filter(name_en=None).update(name_es=F('name'))


def create_filer_plugin(filer_image, target_placeholder, language):
    image_plugin = FilerImage(image=filer_image)
    image_plugin.position = 0
    image_plugin.tree_id = 0
    image_plugin.lft = 0
    image_plugin.rght = 0
    image_plugin.level = 0
    image_plugin.plugin_type = 'FilerImagePlugin'
    image_plugin.language = language
    image_plugin.placeholder = target_placeholder
    image_plugin.save()

    return image_plugin


def create_text_plugin(content_list, target_placeholder, language):

    content_string = ''
    for content in content_list[2:-1]:
        content_string += content

    text = Text(body=content_string)
    text.position = 0
    text.tree_id = None
    text.lft = None
    text.rght = None
    text.level = None
    text.language = language
    text.plugin_type = 'TextPlugin'
    text.placeholder = target_placeholder
    text.save()


def create_news_from_json(language='es'):
    activate(language)

    with open(settings.BASE_DIR + '/gobcl-posts.json') as news:
        json_news = json.loads(news.read())

    app_config = NewsBlogConfig.objects.first()
    owner = User.objects.first()
    author = Person.objects.get_or_create()[0]

    for news in json_news:

        title = news.get('titulo', '')[0]
        image = news.get('thumb_img', '')
        if image:
            image = image[0]
        publishing_date = news.get('fecha', '')[0]
        lead = news.get('bajada', '')
        if lead:
            lead = lead[0]
        content = news.get('contenido', '')

        data = {
            'app_config': app_config,
            'title': title,
            'lead_in': lead,
            'publishing_date': publishing_date,
            'owner': owner,
            'author': author,
            'is_published': True,
        }

        article = Article.objects.create(**data)
        if content:
            create_text_plugin(
                content,
                article.content,
                language
            )
