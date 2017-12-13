"""
Tests for the ministries app
"""

# django
from django.utils.translation import activate, deactivate
# tests
from base.tests import BaseTestCase


class MinisteryTranslationTests(BaseTestCase):
    def test_ministery_model_translation(self):
        """
        Tests that a ministry model is able to be translated
        """
        ministry = self.create_ministry()
        ministry.slug_en = 'ministry-of-mockup'
        ministry.save()
