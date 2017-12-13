import urllib
import random
import string


class ClaveUnicaSettings(object):
    """
    Defines Clave Unica login settings
    """

    TOKEN_LENGHT = 30

    LOGIN_URL = 'https://accounts.claveunica.gob.cl/openid/authorize'

    CLIENT_ID = 'C242172B23D349018620DAE9D39FD8EE'

    CALLBACK_URI = 'https://gobcl.magnet.cl/callback'

    CSRF_PARAMS_DICT = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': CALLBACK_URI,
        'state': '',
        'scope': 'openid run name',
    }

    SECRET_KEY = '  ¯\_(ツ)_/¯  '

    TOKEN_PARAMS_DICT = {
        'client_id': CLIENT_ID,
        'client_secret': SECRET_KEY,
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
