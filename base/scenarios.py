import requests
import json
import uuid
import tempfile

from bs4 import BeautifulSoup

# django
from django.contrib.sites.models import Site
from django.db.models import F
from django.conf import settings
from django.utils.translation import activate
from django.core import files

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
from filer.models.imagemodels import Image
from djangocms_picture.models import Picture


def create_articles(quantity=20, language='en'):
    activate(language)
    app_config = NewsBlogConfig.objects.first()
    m = Mockup()
    for x in range(quantity):
        m.create_article(
            is_published=True,
            app_config=app_config,
        )


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


def create_text_plugin(content, target_placeholder, language, position):
    '''
    Create text plugin by article
    '''

    text = Text(body=content)
    text.position = position
    text.tree_id = None
    text.lft = None
    text.rght = None
    text.level = None
    text.language = language
    text.plugin_type = 'TextPlugin'
    text.placeholder = target_placeholder
    text.save()


def create_picture_plugin(image, target_placeholder, language, position):
    '''
    Create picture image plugin by Article
    '''

    # separate name and path from url image
    image_html = BeautifulSoup(image, 'html.parser')
    image_src = image_html.img.get('src')
    data_image = image_src.split('/')[-3:]

    s3_url = 'https://s3-us-west-2.amazonaws.com/gob.cl/'
    img_url = s3_url + 'gobcl-uploads/' + '/'.join(data_image)

    img = download_file_from_url(img_url)

    if not img:
        return

    img_name = data_image[-1]

    if len(img_name) > 150:
        print('entro al if de 150 content')
        img_name_split = img_name.split('.')
        img_name = '{}.{}'.format(
            str(uuid.uuid4()),
            img_name_split[-1]
        )

    # Create Image element (django CMS)
    image = Image.objects.create()
    image.name = img_name
    image.file.save(
        img_name,
        img,
        save=True
    )
    image.save()

    # Create Picture plugin
    picture = Picture.objects.create()
    picture.picture = image
    picture.position = position
    picture.tree_id = None
    picture.lft = None
    picture.rght = None
    picture.level = None
    picture.language = language
    picture.plugin_type = 'PicturePlugin'
    picture.placeholder = target_placeholder
    picture.save()


def create_content(content_list, target_placeholder, language):
    '''
    Create text or upload image depends content list
    '''

    position = 0
    for content in content_list[2:-1]:
        if content == '\n' or content == '\r\n':
            continue

        elif content.startswith('<p><img'):

            create_picture_plugin(
                content,
                target_placeholder,
                language,
                position
            )

        else:

            create_text_plugin(
                content,
                target_placeholder,
                language,
                position,
            )

        position += 1


def download_file_from_url(url):

    # Stream the image from the url
    try:
        request = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        return

    if request.status_code != requests.codes.ok:
        return

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    return files.File(lf)


def create_news_from_json():
    '''
    Open gobcl-posts.json and read
    data to create news from old site gob.cl
    '''

    # open gobcl-posts.json
    with open(settings.BASE_DIR + '/gobcl-posts.json') as news:
        json_news = json.loads(news.read())

    # get basic data required by model Article (aldryn newsblog)   
    app_config = NewsBlogConfig.objects.first()
    owner = User.objects.first()
    author = Person.objects.get_or_create()[0]

    for news in json_news:

        # Get principal data from json
        title = news.get('titulo', '')[0]
        image_url = news.get('thumb_img', '')
        publishing_date = news.get('fecha', '')[0]
        lead = news.get('bajada', '')
        if lead:
            lead = lead[0]
        content = news.get('contenido', '')
        language = news.get('lang', 'es')

        if language == 'es-CL' or language == 'es':
            activate('es')
            language = 'es'
        elif language == 'en-US':
            activate('en')
            language = 'en'

        article = Article.objects.translated(
            title=title
        )

        if article.exists():
            continue

        data = {
            'app_config': app_config,
            'title': title,
            'lead_in': lead,
            'publishing_date': publishing_date,
            'owner': owner,
            'author': author,
            'is_published': True,
        }

        if image_url:
            # import ipdb ; ipdb.set_trace()

            '''
            if exists image_url get image from
            gobcl-uploads folder and create add image to Article
            '''

            data_image = image_url[0].split('/')[-3:]

            s3_url = 'https://s3-us-west-2.amazonaws.com/gob.cl/'
            img_url = s3_url + 'gobcl-uploads/' + '/'.join(data_image)

            img = download_file_from_url(img_url)
            if img:
                img_name = data_image[-1]

                if len(img_name) > 150:
                    print('entro al if de 150 json')
                    img_name_split = img_name.split('.')
                    img_name = '{}.{}'.format(
                        str(uuid.uuid4()),
                        img_name_split[-1]
                    )

                print('*' * 10)
                print('titulo noticia ' + title)
                print('titulo imagen ' + img_name)
                print('*' * 10)

                image = Image.objects.create()
                image.name = img_name
                image.file.save(
                    img_name,
                    img,
                    save=True
                )
                image.save()
                data['featured_image'] = image

        article = Article.objects.create(**data)

        if content:
            create_content(
                content,
                article.content,
                language
            )
