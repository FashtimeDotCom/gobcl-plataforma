"""
Tests for the regions app
"""

# django
from django.utils.translation import activate
# tests
from base.tests import BaseTestCase


class RegioniTranslationTests(BaseTestCase):
    def test_region_model_translation(self):
        """
        Tests that a region model is able to be translated
        """
        region = self.create_region()
        region.slug_en = 'region-of-mockup'
        region.save()

        activate('es')
        self.assertIn(region.slug_es, region.get_absolute_url())

        activate('en')
        self.assertIn(region.slug_en, region.get_absolute_url())
