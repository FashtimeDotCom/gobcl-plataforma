import requests
import threading
import base64

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from django.conf import settings


class EmailBackend(BaseEmailBackend):
    '''
    Backend email to send emails via gobcl api
    '''

    def __init__(self, **kwargs):
        self.url_send_email = settings.GOBCL_EMAIL_URL_SEND_EMAIL
        self.url_access_token = settings.GOBCL_EMAIL_ACCESS_URL
        self.client_id = settings.GOBCL_EMAIL_CLIENT_ID
        self.client_secret = settings.GOBCL_EMAIL_CLIENT_SECRET
        self.token_app = settings.GOBCL_EMAIL_TOKEN_APP
        self._lock = threading.RLock()
        self.access_token = ''

    def get_access_token(self):
        '''
        Function to get access token
        '''

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'sendmail',
            'grant_type': 'client_credentials'
        }

        try:

            response = requests.post(
                self.url_access_token,
                headers=headers,
                data=payload
            ).json()

            return response['access_token']
        except:
            return None

    def valid_status(self, status_code):
        valid_statuses = (200, 202)
        return status_code in valid_statuses

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return

        with self._lock:
            if not self.access_token:
                self.access_token = self.get_access_token()
            if not self.access_token:
                return 0

            num_sent = 0
            for message in email_messages:
                status_code = self._send(message, self.access_token)

                if self.valid_status(status_code):
                    num_sent += 1
                else:
                    self.new_access_token = self.get_access_token()
                    if (not self.new_access_token or
                            self.new_access_token == self.access_token):
                        self.new_access_token = self.get_access_token()
                    status_code = self._send(message, self.access_token)
                    if self.valid_status(status_code):
                        num_sent += 1

        return num_sent

    def _send(self, email_message, access_token):

        if not email_message.recipients():
            return False

        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        recipients = [
            sanitize_address(addr, encoding)
            for addr in email_message.recipients()
        ]
        subject = base64.b64encode(email_message.subject.encode('UTF-8'))
        message = email_message.message().as_bytes(linesep='\r\n')

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Authorization': 'bearer ' + access_token,
        }

        body = base64.b64encode(message)

        payload = {
            'from': 'no-reply@digital.gob.cl',
            'to': recipients,
            'token_app': self.token_app,
            'subject': subject.decode('ascii'),
            'body': body.decode('ascii')
        }

        response = requests.post(
            self.url_send_email,
            headers=headers,
            json=payload,
        )

        return response.status_code
