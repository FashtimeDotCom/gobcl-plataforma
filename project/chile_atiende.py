import requests


class ChileAtiende(object):

    def __init__(self, access_token):
        self._url = 'http://www.chileatiende.cl/api'
        self._access_token = access_token

    def _connect(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }

        request = requests.get(
            url,
            headers=headers
        )

        return request.json()

    def _get_url(path, id=None):
        return '{}{}'.format(
            self._url,
            path,
        )


class Service(ChileAtiende):

    def list(self):

        url_connection = '{}{}?access_token={}&type=json'.format(
            self._url,
            '/servicios',
            self._access_token,
        )

        return self._connect(url_connection)

    def get(self, service_id):

        url_connection = '{}{}{}?access_token={}&type=json'.format(
            self._url,
            '/servicios/',
            service_id,
            self._access_token,
        )

        return self._connect(url_connection)


class File(ChileAtiende):
