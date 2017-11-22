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

        return request

    def _get_url(self, path, id=None, is_file=False):

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

    def list(self):

        return self._connect(
            self._get_url('/fichas')
        )

    def get(self, file_id):

        return self._connect(
            self._get_url('/fichas', file_id)
        )

    def by_service(self, service_id):

        return self._connect(
            self._get_url('/servicios', service_id, is_file=True)
        )
