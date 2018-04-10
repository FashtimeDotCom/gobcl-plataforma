# standard library imports
import os
import random
import string
import uuid

# django
from django.apps import apps
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate

# third party
from cms.models import Page
from easy_thumbnails.files import get_thumbnailer

# utils
from base.utils import random_string
from inflection import underscore
# from model_mommy import mommy

# models
from articles.models import Article
from aldryn_people.models import Person
from campaigns.models import Campaign
from cms.models.placeholdermodel import Placeholder
from contingencies.models import Contingency
from contingencies.models import ContingencyEvent
from contingencies.models import ContingencyInformation
from filer.models.imagemodels import Image
from gobcl_cms.models import ArticleCount
from gobcl_cms.models import ContentPlugin
from gobcl_cms.models import GalleryImagePlugin
from gobcl_cms.models import GalleryPlugin
from gobcl_cms.models import HeaderImage
from gobcl_cms.models import HeaderPlugin
from gobcl_cms.models import HtmlPlugin
from gobcl_cms.models import PlainTextPlugin
from gobcl_cms.models import SectionPlugin
from government_structures.models import GovernmentStructure
from links.models import FooterLink
from ministries.models import Ministry
from ministries.models import PublicService
from presidencies.models import Presidency
from presidencies.models import PresidencyURL
from public_enterprises.models import PublicEnterprise
from public_servants.models import PublicServant
from regions.models import Commune
from regions.models import Region
from services.models import ChileAtiendeFile
from services.models import ChileAtiendeService
from streams.models import Stream
from streams.models import StreamEvent
from users.models import User
from sociocultural_departments.models import SocioculturalDepartment
from sociocultural_departments.models import SocioculturalDepartmentURL


class Mockup(object):
    def __init__(self):
        super()
        activate('es')

    def create_article(self, **kwargs):
        self.set_required_string(kwargs, 'title')
        self.set_required_foreign_key(kwargs, 'created_by', 'user')
        self.set_required_string(kwargs, 'slug')
        return Article.objects.create(**kwargs)

    def create_government_structure(self, **kwargs):
        self.set_required_datetime(kwargs, 'publication_date')
        return GovernmentStructure.objects.create(**kwargs)

    def create_ministry(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return Ministry.objects.create(**kwargs)

    def create_page(self, **kwargs):
        title = kwargs['reverse_id']

        if 'site_id' not in kwargs:
            kwargs['site_id'] = 1

        page = Page.objects.create(**kwargs)

        for language in ('es', 'en'):
            page.title_set.get_or_create(
                title=title,
                language=language,
                slug=slugify(title),
            )
            page.publish(language)

        return page

    def create_placeholder(self, **kwargs):
        return Placeholder.objects.create(**kwargs)

    def create_public_service(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'ministry')
        return PublicService.objects.create(**kwargs)

    def create_user(self, **kwargs):
        self.set_required_email(kwargs, 'email')
        self.set_required_string(kwargs, 'first_name')
        self.set_required_string(kwargs, 'last_name')
        self.set_required_rut(kwargs, 'rut')
        return User.objects.create(**kwargs)

    def create_person(self, **kwargs):
        return Person.objects.create(**kwargs)

    def create_public_servant(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return PublicServant.objects.create(**kwargs)

    def create_presidency(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'government_structure')
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'description')
        self.set_required_string(kwargs, 'twitter')
        self.set_required_url(kwargs, 'url')

        if 'photo' not in kwargs:
            test_root = os.path.realpath(os.path.dirname(__file__))
            photo = open('{}/tests/gondola.jpg'.format(test_root), 'rb')
            photo = get_thumbnailer(photo, relative_name='photos/gondola.jpg')
            kwargs['photo'] = photo

        return Presidency.objects.create(**kwargs)

    def create_commune(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'region')
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_email(kwargs, 'email')
        self.set_required_phone_number(kwargs, 'phone')
        self.set_required_string(kwargs, 'twitter')
        self.set_required_url(kwargs, 'url')
        self.set_required_boolean(kwargs, 'has_own_municipality')
        return Commune.objects.create(**kwargs)

    def create_presidency_url(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        return PresidencyURL.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_slug(kwargs, 'slug')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return Region.objects.create(**kwargs)

    def create_campaign(self, **kwargs):
        self.set_required_string(kwargs, 'title')
        self.set_required_foreign_key(kwargs, 'image')
        self.set_required_url(kwargs, 'external_url')
        return Campaign.objects.create(**kwargs)

    def create_image(self, **kwargs):
        return Image.objects.create(**kwargs)

    def create_footer_link(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return FooterLink.objects.create(**kwargs)

    def create_public_enterprise(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return PublicEnterprise.objects.create(**kwargs)

    def create_chile_atiende_service(self, **kwargs):
        self.set_required_string(kwargs, 'code')
        self.set_required_string(kwargs, 'mision')
        return ChileAtiendeService.objects.create(**kwargs)

    def create_chile_atiende_file(self, **kwargs):
        self.set_required_foreign_key(
            kwargs,
            'service',
            model='chile_atiende_service',
        )
        self.set_required_string(kwargs, 'service_name')
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'code')
        self.set_required_string(kwargs, 'objective')
        self.set_required_string(kwargs, 'beneficiaries')
        self.set_required_string(kwargs, 'cost')
        self.set_required_string(kwargs, 'period')
        self.set_required_string(kwargs, 'duration')
        self.set_required_int(kwargs, 'analytic_visits', minimum=1)
        return ChileAtiendeFile.objects.create(**kwargs)

    def create_header_image(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        return HeaderImage.objects.create(**kwargs)

    def create_header_plugin(self, **kwargs):
        return HeaderPlugin.objects.create(**kwargs)

    def create_content_plugin(self, **kwargs):
        return ContentPlugin.objects.create(**kwargs)

    def create_article_count(self, **kwargs):
        return ArticleCount.objects.create(**kwargs)

    def create_contingency(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'lead')
        self.set_required_string(kwargs, 'description')
        return Contingency.objects.create(**kwargs)

    def create_contingency_event(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'contingency')
        self.set_required_string(kwargs, 'title')
        self.set_required_url(kwargs, 'url')
        self.set_required_datetime(kwargs, 'date_time')
        return ContingencyEvent.objects.create(**kwargs)

    def create_contingency_information(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'contingency')
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        return ContingencyInformation.objects.create(**kwargs)

    def create_gallery_plugin(self, **kwargs):
        self.set_required_string(kwargs, 'description')
        return GalleryPlugin.objects.create(**kwargs)

    def create_gallery_image_plugin(self, **kwargs):
        return GalleryImagePlugin.objects.create(**kwargs)

    def create_html_plugin(self, **kwargs):
        self.set_required_string(kwargs, 'html')
        return HtmlPlugin.objects.create(**kwargs)

    def create_plain_text_plugin(self, **kwargs):
        self.set_required_string(kwargs, 'text')
        return PlainTextPlugin.objects.create(**kwargs)

    def create_section_plugin(self, **kwargs):
        self.set_required_string(kwargs, 'title')
        return SectionPlugin.objects.create(**kwargs)

    def create_stream(self, **kwargs):
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        return Stream.objects.create(**kwargs)

    def create_stream_event(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'stream')
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'description')
        self.set_required_datetime(kwargs, 'date_time')
        return StreamEvent.objects.create(**kwargs)

    def create_sociocultural_department(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'government_structure')
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'title')
        self.set_required_string(kwargs, 'description')
        self.set_required_string(kwargs, 'twitter')
        self.set_required_url(kwargs, 'url')

        if 'photo' not in kwargs:
            test_root = os.path.realpath(os.path.dirname(__file__))
            photo = open('{}/tests/gondola.jpg'.format(test_root), 'rb')
            photo = get_thumbnailer(photo, relative_name='photos/gondola.jpg')
            kwargs['photo'] = photo
        return SocioculturalDepartment.objects.create(**kwargs)

    def create_sociocultural_department_url(self, **kwargs):
        return SocioculturalDepartmentURL.objects.create(**kwargs)

    def get_or_create_page(self, **kwargs):
        try:
            return Page.objects.get(
                reverse_id=kwargs['reverse_id'],
                site_id=kwargs['site_id'],
            ), False
        except Page.DoesNotExist:
            pass
        except Page.MultipleObjectsReturned:
            return Page.objects.filter(**kwargs).first(), False

        return self.create_page(**kwargs), True

    #
    def random_email(self):
        return "{}@{}.{}".format(
            self.random_string(length=6),
            self.random_string(length=6),
            self.random_string(length=2)
        )

    def random_hex_int(self, *args, **kwargs):
        val = self.random_int(*args, **kwargs)
        return hex(val)

    def random_int(self, minimum=-100000, maximum=100000):
        return random.randint(minimum, maximum)

    def random_float(self, minimum=-100000, maximum=100000):
        return random.uniform(minimum, maximum)

    def random_rut(self):
        return '{}.{}.{}-{}'.format(
            self.random_int(minimum=1, maximum=99),
            self.random_int(minimum=100, maximum=990),
            self.random_int(minimum=100, maximum=990),
            self.random_string(length=1, chars='k' + string.digits),
        )

    def random_string(self, length=6, chars=None):
        return random_string(length=length, chars=chars)

    def random_uuid(self, *args, **kwargs):
        chars = string.digits
        return uuid.UUID(''.join(random.choice(chars) for x in range(32)))

    def random_phone_number(self, *args, **kwargs):
        chars = string.digits
        return '+5698'.join(random.choice(chars) for x in range(7))

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:

            if default is None:
                data[field] = not not random.randint(0, 1)
            else:
                data[field] = default

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

    def set_required_phone_number(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_phone_number()

    def set_required_datetime(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now()

    def set_required_email(self, data, field):
        if field not in data:
            data[field] = self.random_email()

    def set_required_float(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_float(**kwargs)

    def set_required_foreign_key(self, data, field, model=None, **kwargs):
        if model is None:
            model = field

        if field not in data and '{}_id'.format(field) not in data:
            data[field] = getattr(self, 'create_{}'.format(model))(**kwargs)

    def set_required_image(self, data, field, **kwargs):
        if field not in data:
            test_root = os.path.realpath(os.path.dirname(__file__))
            photo = open('{}/tests/gondola.jpg'.format(test_root), 'rb')
            photo = get_thumbnailer(photo, relative_name='photos/gondola.jpg')
            data[field] = photo

    def set_required_int(self, data, field, **kwargs):
        if field not in data:
            data[field] = self.random_int(**kwargs)

    def set_required_ip_address(self, data, field, **kwargs):
        if field not in data:
            ip = '{}.{}.{}.{}'.format(
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
                self.random_int(minimum=1, maximum=255),
            )
            data[field] = ip

    def set_required_rut(self, data, field):
        if field not in data:
            data[field] = self.random_rut()

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_slug(self, data, field, length=6):
        if field not in data:
            data[field] = slugify(self.random_string(length=length))

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))


def add_get_or_create(cls, model):
    model_name = underscore(model.__name__)
    method_name = 'create_{}'.format(model_name)

    # if not hasattr(cls, method_name):

    #     def create_obj(self, *args, **kwargs):
    #         return mommy.make(model)

    #     setattr(cls, method_name, create_obj)

    def get_or_create(self, **kwargs):
        try:
            return model.objects.get(**kwargs), False
        except model.DoesNotExist:
            pass

        return getattr(cls, method_name)(self, **kwargs), True

    get_or_create.__doc__ = "Get or create for {}".format(model_name)
    get_or_create.__name__ = "get_or_create_{}".format(model_name)
    setattr(cls, get_or_create.__name__, get_or_create)


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


for model in get_our_models():
    add_get_or_create(Mockup, model)
