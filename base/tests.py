"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# standard library
import uuid

# django
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.utils.translation import activate
from django.utils import timezone

# urls
from project.urls import urlpatterns

# utils
from inflection import underscore
from base.utils import get_our_models
from base.mockups import Mockup
from base.scenarios import get_current_government_structure
from base.scenarios import create_presidency

# Third-party app imports
from model_mommy import mommy
from model_mommy import random_gen


class BaseTestCase(TestCase, Mockup):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        activate('es')

        self.password = random_gen.gen_text()
        self.user = mommy.prepare('users.User')
        self.user.set_password(self.password)
        self.user.save()

        self.login()

    def login(self, user=None, password=None):
        if user is None:
            user = self.user
            password = self.password

        return self.client.login(email=user.email, password=password)


class IntegrityOnDeleteTestCase(BaseTestCase):
    def create_full_object(self, model):
        kwargs = {}
        for f in model._meta.fields:

            if isinstance(f, models.fields.related.ForeignKey) and f.null:
                model_name = f.rel.to.__name__
                if model_name == 'Campaign':
                    kwargs[f.name] = mommy.make(
                        f.rel.to, title='foo', description='')
                elif model_name == 'Image':
                    kwargs[f.name] = mommy.make(
                        f.rel.to, uploaded_at=timezone.now())
                elif model_name == 'Ministry' or model_name == 'Region':
                    name = str(uuid.uuid4())
                    kwargs[f.name] = mommy.make(
                        f.rel.to, name=name, description='')
                else:
                    kwargs[f.name] = mommy.make(f.rel.to)

        try:
            return mommy.make(model, **kwargs), kwargs

        except:
            kwargs['name'] = str(uuid.uuid4())

            kwargs_complete = kwargs
            del kwargs['name']
            return mommy.make(model, **kwargs_complete), kwargs

    def test_integrity_on_delete(self):

        for model in get_our_models():
            # ignore gobcl_cms
            if (model._meta.app_label == 'gobcl_cms' or
                    model.__name__ == 'CampaignTranslation'):
                continue

            obj, related_nullable_objects = self.create_full_object(model)

            obj_count = model.objects.count()

            for relation_name, rel_obj in related_nullable_objects.items():

                try:
                    # check if the test should be skipped
                    if relation_name in obj.exclude_on_on_delete_test:
                        continue
                except AttributeError:
                    pass

                if model.__name__.endswith('Translation'):
                    continue

                rel_obj.delete()

                error_msg = (
                    '<{}> object, was deleted after deleting a nullable '
                    'related <{}> object, the relation was "{}"'
                ).format(model.__name__, rel_obj.__class__.__name__,
                         relation_name)

                self.assertEqual(obj_count, model.objects.count(), error_msg)


def reverse_pattern(pattern, namespace, args=None, kwargs=None):
    try:
        if namespace:
            return reverse('{}:{}'.format(
                namespace, pattern.name, args=args, kwargs=kwargs)
            )
        else:
            return reverse(pattern.name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None


class UrlsTest(BaseTestCase):

    def setUp(self):
        super(UrlsTest, self).setUp()

        # it is mandatory for this project to always have an
        # active government_structure and presidency.
        get_current_government_structure()
        create_presidency()

        # we are going to send parameters, so one thing we'll do is to send
        # tie id 1
        self.user.delete()
        self.user.id = 1

        # give the user all the permissions, so we test every page
        self.user.is_superuser = True

        self.user.save()
        self.login()

        self.default_params = {}

        for model in get_our_models():
            model_name = underscore(model.__name__)
            method_name = 'create_{}'.format(model_name)
            param_name = '{}_id'.format(model_name)

            if model_name.endswith('_translation'):
                continue
            elif model_name == 'campaign':
                obj = mommy.make(model, title='foo')
            elif model_name == 'ministry' or model_name == 'region':
                name = str(uuid.uuid4())
                obj = mommy.make(
                    model, name=name, description='')
            else:
                obj = mommy.make(model)

            self.assertIsNotNone(obj, '{} returns None'.format(method_name))

            self.default_params[param_name] = obj.id

    def reverse_pattern(self, pattern, namespace):
        url = reverse_pattern(pattern, namespace)

        if url is None:
            reverse_pattern(pattern, namespace, args=(1,))

            if url is None:
                reverse_pattern(pattern, namespace, args=(1, 1))

        if url is None:
            return None

        view_params = resolve(url).kwargs

        for param in view_params:
            try:
                view_params[param] = self.default_params[param]
            except KeyError:
                pass

        return reverse_pattern(pattern, namespace, kwargs=view_params)

    def test_responses(self):

        ignored_namespaces = []

        ignored_urls = [
            "/noticias/",
            "/news/",
            "/admin/filer/clipboard/operations/upload/no_folder/",
        ]

        def test_url_patterns(patterns, namespace=''):

            if namespace in ignored_namespaces:
                print('Ignored namespace: {}.'.format(namespace))
                return

            for pattern in patterns:
                self.login()

                if hasattr(pattern, 'name'):
                    url = self.reverse_pattern(pattern, namespace)

                    if not url:
                        continue

                    for ignored_url in ignored_urls:
                        if ignored_url in url:
                            print('ignored url: {}'.format(url))
                            return

                    try:
                        response = self.client.get(url)
                    except:
                        print("Url {} failed: ".format(url))
                        raise

                    msg = 'url "{}" returned {}'.format(
                        url, response.status_code
                    )

                    if response.status_code == 500:
                        print(url)
                        print(response.content)

                    self.assertIn(
                        response.status_code,
                        (200, 302, 403), msg
                    )
                else:
                    test_url_patterns(pattern.url_patterns, pattern.namespace)

        test_url_patterns(urlpatterns)

        for model, model_admin in admin.site._registry.items():
            patterns = model_admin.get_urls()
            test_url_patterns(patterns, namespace='admin')
