"""Login Bypass integration.
"""

import json
import logging
import requests

from django.conf import settings

LOGIN_BYPASS_URL = 'http://www.pbslearningmedia.org/bypass/create_token/'


log = logging.getLogger(__name__)


def get_redirect(url, user_id, email, first_name=None, last_name=None):
    """Retreive a redirect URL from the Login Bypass API.
    """

    payload = {
        'key': settings.LOGIN_BYPASS_KEY,
        'user_id': user_id,
        'email': email,
        'lm_url': url,
        'first_name': first_name,
        'last_name': last_name,
    }

    response = requests.post(LOGIN_BYPASS_URL, data=payload)

    # The Login Bypass API layers in status codes with JSON responses.  So it's
    # possible to get a good response from the server but have it show up with
    # 4xx status code.

    data = response.json()

    if 'redirect_url' in data:
        log.debug("Login Bypass API success.  Returning redirect: %s", data['redirect_url'])
        return data['redirect_url']

    else:
        log.error("Login Bypass API did not return a redirect url.")
        log.error(json.dumps(data, indent=4))
        raise Exception(
           "Unable to retrieve a redirect URL from Login Bypass API."
        )

