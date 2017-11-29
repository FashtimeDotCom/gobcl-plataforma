# standard library imports
import os
import random
import string
import uuid

# django
from django.apps import apps
from django.utils import timezone
from django.utils.text import slugify
from easy_thumbnails.files import get_thumbnailer

# cms
from cms.models import Page

# utils
from base.utils import random_string
from inflection import underscore
from model_mommy import mommy

# models
from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from public_servants.models import PublicServant
from regions.models import Region
from presidencies.models import Presidency
from campaigns.models import Campaign
from filer.models.imagemodels import Image
from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from users.models import User
from aldryn_people.models import Person


class Mockup(object):

    def create_government_structure(self, **kwargs):
        self.set_required_datetime(kwargs, 'publication_date')
        return GovernmentStructure.objects.create(**kwargs)

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

    def create_user(self, **kwargs):
        self.set_required_email(kwargs, 'email')
        self.set_required_string(kwargs, 'first_name')
        self.set_required_string(kwargs, 'last_name')
        return User.objects.create(**kwargs)

    def create_article(self, **kwargs):
        self.set_required_string(kwargs, 'title')
        self.set_required_foreign_key(kwargs, 'app_config')
        self.set_required_foreign_key(kwargs, 'owner', 'user')
        self.set_required_foreign_key(kwargs, 'author', 'person')
        return Article.objects.create(**kwargs)

    def create_person(self, **kwargs):
        return Person.objects.create(**kwargs)

    def create_app_config(self, **kwargs):
        self.set_required_string(kwargs, 'namespace')
        return NewsBlogConfig.objects.create(**kwargs)

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

    def create_ministry(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return Ministry.objects.create(**kwargs)

    def create_region(self, **kwargs):
        self.set_required_string(kwargs, 'name')
        self.set_required_string(kwargs, 'description')
        self.set_required_url(kwargs, 'url')
        self.set_required_foreign_key(kwargs, 'government_structure')
        return Region.objects.create(**kwargs)

    def create_campaign(self, **kwargs):
        self.set_required_foreign_key(kwargs, 'image')
        return Campaign.objects.create(**kwargs)

    def create_image(self, **kwargs):
        return Image.objects.create(**kwargs)

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

    def random_string(self, length=6, chars=None):
        return random_string(length=length, chars=chars)

    def random_uuid(self, *args, **kwargs):
        chars = string.digits
        return uuid.UUID(''.join(random.choice(chars) for x in range(32)))

    def set_required_boolean(self, data, field, default=None, **kwargs):
        if field not in data:

            if default is None:
                data[field] = not not random.randint(0, 1)
            else:
                data[field] = default

    def set_required_date(self, data, field, **kwargs):
        if field not in data:
            data[field] = timezone.now().date()

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

    def set_required_rut(self, data, field, length=6):
        if field not in data:
            rut = '{}.{}.{}-{}'.format(
                self.random_int(minimum=1, maximum=99),
                self.random_int(minimum=100, maximum=990),
                self.random_int(minimum=100, maximum=990),
                self.random_string(length=1, chars='k' + string.digits),
            )
            data[field] = rut

    def set_required_string(self, data, field, length=6):
        if field not in data:
            data[field] = self.random_string(length=length)

    def set_required_url(self, data, field, length=6):
        if field not in data:
            data[field] = 'http://{}.com'.format(
                self.random_string(length=length))


def add_get_or_create(cls, model):
    model_name = underscore(model.__name__)
    method_name = 'create_{}'.format(model_name)

    if not hasattr(cls, method_name):

        def create_obj(self, *args, **kwargs):
            return mommy.make(model)

        setattr(cls, method_name, create_obj)

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
