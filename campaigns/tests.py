from base.tests import BaseTestCase

from .models import Campaign
from cms.models.pagemodel import Page
from django.contrib.sites.models import Site
from cms.models.titlemodels import Title


class CampaignModelTest(BaseTestCase):
    '''
    Test for model campaign
    '''

    def setUp(self):
        pass

    def test_campaign_with_url(self):
        '''
        Test create only campaign without CMS page
        '''

        self.assertEqual(Campaign.objects.count(), 0)
        self.assertEqual(Page.objects.count(), 0)

        external_url = 'http://example.com'
        self.campaign = self.create_campaign(
            external_url=external_url
        )

        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Page.objects.count(), 0)
        self.assertEqual(
            self.campaign.get_absolute_url(),
            external_url
        )

    def test_campaign_without_url(self):
        '''
        Test create CMS page when create campaign without external url
        '''
        self.assertEqual(Campaign.objects.count(), 0)
        self.assertEqual(Page.objects.count(), 0)

        campaign = self.create_campaign(
            title='foo',
        )

        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(Title.objects.count(), 1)

        page = Page.objects.get()
        title = Title.objects.get()

        self.assertEqual(page.template, 'campaigns/campaign_detail.pug')
        self.assertEqual(page.site, Site.objects.get_current())
        self.assertEqual(campaign.page, page)
        self.assertEqual(
            campaign.get_absolute_url(),
            page.get_absolute_url()
        )
        self.assertEqual(title.published, campaign.is_active)
        self.assertEqual(title.title, campaign.title)
        self.assertFalse(page.in_navigation)
