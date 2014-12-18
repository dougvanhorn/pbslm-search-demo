"""Login Bypass integration.
"""

import json
import logging
import requests

from django.conf import settings

LOGIN_BYPASS_URL = 'http://www.pbslearningmedia.org/bypass/create_token/'
LOGIN_BYPASS_URL = 'http://panda.example.com/bypass/create_token/'


log = logging.getLogger(__name__)


class LoginBypassError(Exception):
    """Generic exception for Login Bypass.

    Attributes:
        response: the `requests.Response` from the API.

    
    """
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return repr(self.response)


def get_redirect(url, user_id, email, first_name=None, last_name=None,
                 postal_code=None):
    """Retreive a redirect URL from the Login Bypass API.
    """

    payload = {
        'key': settings.LOGIN_BYPASS_KEY,
        'user_id': user_id,
        'email': email,
        'lm_url': url,
        'first_name': first_name,
        'last_name': last_name,
        'postal_code': postal_code,
    }

    response = requests.post(LOGIN_BYPASS_URL, data=payload)

    # The Login Bypass API layers in status codes with JSON responses.  So it's
    # possible to get a good response from the server but have it show up with
    # 4xx status code.

    if not response.ok:
        log.debug("POSTing to %s.", LOGIN_BYPASS_URL)
        log.debug("Payload: %s", payload)
        log.debug("Status Code: {}".format(response.status_code))
        log.error("Login Bypass API did not return a redirect url.")
        log.error(response.text)
        exc = LoginBypassError(response=response)
        raise exc

    data = response.json()

    log.debug("Login Bypass API success.  Returning redirect: %s", data['redirect_url'])
    return data['redirect_url']

