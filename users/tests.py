"""
Tests for the user app
"""
# standard
import json

# django
from django.core.urlresolvers import reverse

# tests
from base.tests import BaseTestCase


class UserTests(BaseTestCase):
    def test_lower_case_emails(self):
        """
        Tests that users are created with lower case emails
        """
        self.user.email = "Hello@magnet.cl"
        self.user.save()
        self.assertEqual(self.user.email, 'hello@magnet.cl')

    def test_force_logout(self):
        """
        Tests that users are created with lower case emails
        """
        url = reverse('password_change')
        response = self.client.get(url)

        # test that the user is logged in
        self.assertEqual(response.status_code, 200)

        self.user.force_logout()

        response = self.client.get(url)

        # user is logged out, sow redirects to login
        self.assertEqual(response.status_code, 302)


class UserFontSizeTests(BaseTestCase):
    def test_font_size_increase(self):
        """
        Tests that a user can increase font size
        """
        url = reverse('user_font_size_change')
        data = {
            'type': 'increase',
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response_dict = json.loads(
            str(response.content, encoding='utf-8')
        )

        self.assertEqual(response_dict['changed'], True)
        self.assertEqual(response_dict['size'], 'l')

    def test_font_size_decrease(self):
        """
        Tests that a user can decrease font size
        """
        url = reverse('user_font_size_change')
        data = {
            'type': 'decrease',
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response_dict = json.loads(
            str(response.content, encoding='utf-8')
        )

        self.assertEqual(response_dict['changed'], True)
        self.assertEqual(response_dict['size'], 's')
