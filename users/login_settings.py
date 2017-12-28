# standard
import os
import random
import string
import urllib

# django
from django.conf import settings

# local settings
if 'DOCKER' in os.environ:
    from project.production.local_settings import CLAVE_UNICA_CALLBACK
    from project.production.local_settings import CLAVE_UNICA_CLIENT_ID
elif 'STAGING' in os.environ:
    from project.staging.local_settings import CLAVE_UNICA_CALLBACK
    from project.staging.local_settings import CLAVE_UNICA_CLIENT_ID
else:
    from project.local_settings import CLAVE_UNICA_CALLBACK
    from project.local_settings import CLAVE_UNICA_CLIENT_ID


class ClaveUnicaSettings(object):
    """
    Defines Clave Unica login settings
    """

    TOKEN_LENGHT = 30

    LOGIN_URL = 'https://accounts.claveunica.gob.cl/openid/authorize'

    CLIENT_ID = CLAVE_UNICA_CLIENT_ID

    CALLBACK_URI = CLAVE_UNICA_CALLBACK

    CSRF_PARAMS_DICT = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': CALLBACK_URI,
        'state': '',
        'scope': 'openid run name email',
    }

    CLAVEUNICA_SECRET_KEY = settings.CLAVEUNICA_SECRET_KEY

    TOKEN_PARAMS_DICT = {
        'client_id': CLIENT_ID,
        'client_secret': CLAVEUNICA_SECRET_KEY,
        'redirect_uri': CALLBACK_URI,
        'grant_type': 'authorization_code',
        'code': '',
        'state': '',
    }

    TOKEN_URI = 'https://accounts.claveunica.gob.cl/openid/token/'
    USER_INFO_URI = 'https://www.claveunica.gob.cl/openid/userinfo/'

    def generate_token(self):
        return ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits)
            for i in range(self.TOKEN_LENGHT)
        )
        pass

    def get_csrf_redirect_url(self, token=None):
        if not token:
            token = self.generate_token()
        self.CSRF_PARAMS_DICT['state'] = token

        return '{}?{}'.format(
            self.LOGIN_URL,
            urllib.parse.urlencode(self.CSRF_PARAMS_DICT),
        )

    def get_token_url_data(self, state, code):
        data = self.TOKEN_PARAMS_DICT
        data['state'] = state
        data['code'] = code
        return data
