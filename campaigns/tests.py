from base.tests import BaseTestCase

# django
from django.core.urlresolvers import reverse

from .models import Campaign


class CampaignModelTest(BaseTestCase):
    '''
    Test for model campaign
    '''

    def setUp(self):
        pass

    def test_campaign_with_url(self):
        '''
        Test create only campaign with an external url
        '''

        self.assertEqual(Campaign.objects.count(), 0)

        external_url = 'http://example.com'
        self.campaign = self.create_campaign(
            external_url=external_url
        )

        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(
            self.campaign.get_absolute_url(),
            external_url
        )

    def test_campaign_without_url(self):
        '''
        Test create a campaign without an external url
        '''
        self.assertEqual(Campaign.objects.count(), 0)

        self.campaign = self.create_campaign(
            title='foo',
            external_url='',
        )

        self.assertEqual(Campaign.objects.count(), 1)

        self.assertEqual(
            self.campaign.get_absolute_url(),
            reverse('campaigns:campaign_detail', args=(self.campaign.slug,))
        )
