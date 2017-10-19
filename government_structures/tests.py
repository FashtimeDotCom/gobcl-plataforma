from django.utils import timezone

from base.tests import BaseTestCase

from .models import GovernmentStructure
from regions.models import Region


class GovernmentStructureModelTest(BaseTestCase):

    def setUp(self):
        GovernmentStructure.objects.all().delete()
        self.now = timezone.datetime.now()
        self.government_structure = self.create_government_structure(
            publication_date=self.now)
        self.public_servant = self.create_public_servant(
            government_structure=self.government_structure)
        self.region = self.create_region(
            governor=self.public_servant,
            government_structure=self.government_structure)

    def test_duplicate_government_structure_with_existing_date(self):
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.government_structure.duplicate(date=self.now)
        self.assertEqual(GovernmentStructure.objects.count(), 1)

    def test_duplicate_government_with_public_servants(self):
        tomorrow = self.now + timezone.timedelta(days=1)
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.assertEqual(Region.objects.count(), 1)
        self.government_structure.duplicate(date=tomorrow)
        self.assertEqual(GovernmentStructure.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)
