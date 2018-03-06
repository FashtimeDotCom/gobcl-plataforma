from base.tests import BaseTestCase
from django.conf import settings

from .chile_atiende import Service
from .chile_atiende import File


class ChileAtiendeClient(BaseTestCase):

    '''
    Test Chile Atiende API Client
    '''

    def setUp(self):
        self.base_url = 'https://www.chileatiende.gob.cl/api'
        self.access_token = settings.CHILEATIENDE_ACCESS_TOKEN
        self.service_id = self.get_service_id()
        self.file_id = self.get_file_id()

    def get_service_id(self):
        service = Service()
        response = service.list()
        try:
            service_object = response.json()
        except:
            service_object = {
                'servicios': {
                    'items': {
                        'servicio': [{
                            'id': 1,
                        }]
                    }
                }
            }
        service_id = service_object['servicios']['items']['servicio'][0]['id']
        return service_id

    def get_file_id(self):
        file_object = File()
        files = file_object.parsed_list()

        file_id = files[0]['id']
        return file_id

    def test_service_list_ok(self):

        service = Service()
        response = service.list()

        self.assertIn(response.status_code, (200, 403))

        self.assertEqual(
            response.url,
            '{}/servicios?access_token={}&type=json'.format(
                self.base_url,
                self.access_token
            )
        )

    def test_service_get_ok(self):
        service = Service()

        response = service.get(self.service_id)

        self.assertIn(response.status_code, (200, 403))

        self.assertEqual(
            response.url,
            '{}/servicios/{}/?access_token={}&type=json'.format(
                self.base_url,
                self.service_id,
                self.access_token,
            )
        )

    def test_file_list_ok(self):

        file_object = File()
        response = file_object.list()

        self.assertIn(response.status_code, (200, 403))

        self.assertEqual(
            response.url,
            '{}/fichas?access_token={}&type=json'.format(
                self.base_url,
                self.access_token
            )
        )

    def test_file_get_ok(self):
        file_object = File()

        response = file_object.get(self.file_id)

        self.assertIn(response.status_code, (200, 403))

        self.assertEqual(
            response.url,
            '{}/fichas/{}/?access_token={}&type=json'.format(
                self.base_url,
                self.file_id,
                self.access_token,
            )
        )

    def test_file_list_by_service(self):

        file_object = File()

        response = file_object.by_service(self.service_id)

        self.assertIn(response.status_code, (200, 403))

        self.assertEqual(
            response.url,
            '{}/servicios/{}/fichas/?access_token={}&type=json'.format(
                self.base_url,
                self.service_id,
                self.access_token,
            )
        )
