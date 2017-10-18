from django.utils import timezone

from base.tests import BaseTestCase
from model_mommy import mommy

from .models import Government
from regions.models import Region


class GovernmentModelTest(BaseTestCase):

    def setUp(self):
        super(GovernmentModelTest, self).setUp()
        Government.objects.all().delete()
        self.government = mommy.make(Government)
        self.region = mommy.make(
            Region,
            government=self.government
        )

    def test_no_duplicate_government_with_unique_date(self):
        self.assertEqual(Government.objects.count(), 1)
        self.government.duplicate(date=timezone.datetime.now())
        self.assertEqual(Government.objects.count(), 1)

    def test_duplicate_with_public_servant(self):
        tomorrow = timezone.datetime.now() + timezone.timedelta(days=2)
        self.assertEqual(Government.objects.count(), 1)
        self.assertEqual(Region.objects.count(), 1)
        self.government.duplicate(date=tomorrow)
        self.assertEqual(Government.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)
