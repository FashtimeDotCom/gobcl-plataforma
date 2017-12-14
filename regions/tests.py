"""
Tests for the regions app
"""

# django
from django.utils.translation import activate, deactivate
# tests
from base.tests import BaseTestCase


class RegionTranslationTests(BaseTestCase):
    def test_region_model_translation(self):
        """
        Tests that a region model is able to be translated
        """
        region = self.create_region()
        region.slug_en = 'region-of-mockup'
        region.save()
