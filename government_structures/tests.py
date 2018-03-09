from django.utils import timezone

from base.tests import BaseTestCase

from .models import GovernmentStructure
from regions.models import Region
from public_servants.models import PublicServant
from ministries.models import Ministry


class GovernmentStructureModelTest(BaseTestCase):

    def setUp(self):
        GovernmentStructure.objects.all().delete()
        self.now = timezone.now()
        self.government_structure = self.create_government_structure(
            publication_date=self.now)

        self.public_servant = self.create_public_servant(
            government_structure=self.government_structure)
        self.region = self.create_region(
            governor=self.public_servant,
            government_structure=self.government_structure)

        self.public_servant2 = self.create_public_servant(
            government_structure=self.government_structure)
        self.ministry = self.create_ministry(
            minister=self.public_servant2,
            government_structure=self.government_structure)

        self.public_servant3 = self.create_public_servant(
            government_structure=self.government_structure)
        self.ministry2 = self.create_ministry(
            minister=self.public_servant3,
            government_structure=self.government_structure)

    def test_duplicate_government_structure_with_existing_date(self):
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.government_structure.duplicate(date=self.now)
        self.assertEqual(GovernmentStructure.objects.count(), 1)

    def test_duplicate_government_with_public_servants(self):
        tomorrow = self.now + timezone.timedelta(days=1)
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.assertEqual(PublicServant.objects.count(), 3)
        self.assertEqual(Region.objects.count(), 1)
        self.government_structure.duplicate(date=tomorrow)
        self.assertEqual(GovernmentStructure.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)
        self.assertEqual(PublicServant.objects.count(), 6)

    def test_duplicate_government_withouth_public_servants(self):
        tomorrow = self.now + timezone.timedelta(days=1)
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.assertEqual(PublicServant.objects.count(), 3)
        self.assertEqual(Region.objects.count(), 1)
        self.government_structure.duplicate(
            date=tomorrow, with_public_servants=False)
        self.assertEqual(GovernmentStructure.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)

        government_structure = GovernmentStructure.objects.last()
        regions = Region.objects.by_government_structure(government_structure)

        for region in regions:
            self.assertEqual(region.governor, None)

        ministries = Ministry.objects.by_government_structure(
            government_structure)

        for ministry in ministries:
            self.assertEqual(ministry.minister, None)
            self.assertEqual(list(ministry.public_servants.all()), [])

        self.assertEqual(PublicServant.objects.count(), 3)

    def test_duplicate(self):
        tomorrow = self.now + timezone.timedelta(days=1)
        self.assertEqual(GovernmentStructure.objects.count(), 1)
        self.assertEqual(Ministry.objects.count(), 2)
        self.assertEqual(PublicServant.objects.count(), 3)
        self.assertEqual(Region.objects.count(), 1)

        self.government_structure.duplicate(date=tomorrow)

        self.assertEqual(GovernmentStructure.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)
        self.assertEqual(Ministry.objects.count(), 4)
        self.assertEqual(PublicServant.objects.count(), 6)
