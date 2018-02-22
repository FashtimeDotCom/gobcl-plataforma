import requests

from django.conf import settings


class ChileAtiende(object):

    def __init__(self):
        self._url = 'https://www.chileatiende.gob.cl/api'
        self._access_token = settings.CHILEATIENDE_ACCESS_TOKEN

    def _connect(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        request = requests.get(
            url,
            headers=headers
        )

        return request

    def _get_url(self, path, id=None, is_file=False, query=None):

        url = '{}{}'.format(
            self._url,
            path,
        )
        if id:
            url = '{}/{}/'.format(
                url,
                id,
            )

        if is_file:
            url = '{}{}'.format(
                url,
                'fichas/'
            )

        url = '{}?access_token={}&type=json'.format(
                url,
                self._access_token,
            )

        if query:
            url = '{}&query={}'.format(
                url,
                query,
            )

        return url


class Service(ChileAtiende):

    def list(self):

        return self._connect(
            self._get_url('/servicios')
        )

    def get(self, service_id):

        return self._connect(
            self._get_url('/servicios', service_id)
        )


class File(ChileAtiende):

    def list(self, query=None):

        return self._connect(
            self._get_url('/fichas', query=query)
        )

    def get(self, file_id):

        return self._connect(
            self._get_url('/fichas', file_id)
        )

    def by_service(self, service_id):

        return self._connect(
            self._get_url('/servicios', service_id, is_file=True)
        )
