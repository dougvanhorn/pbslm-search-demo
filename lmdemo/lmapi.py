"""Library to use the Search API.
"""

import requests

from django.conf import settings


SEARCH = "http://api-qa.pbslm.org/api/v2/search/"
LO = "http://api-qa.pbslm.org/api/v2/lo/"

AUTHORIZATION = {'Authorization': 'ApiKey %s:%s' % (
    settings.LMAPI_USERNAME, settings.LMAPI_APIKEY)
}


"""API Feedback:

copywright is spelled wrong.

Do we want to show the media_urls?
"""


def get_session():
    """Construct a `requests.Session` instance with authorization.
    """
    session = requests.Session()
    session.headers.update(AUTHORIZATION)
    return session


def search(q, facets=None):
    """Perform a search.

    q -- the query string to search
    facets -- list of facets to use in query.

    Returns a `requests.Response` instance.
    """
    if facets is None:
        facets = []

    session = get_session()
    parameters = {
        'expanded': 'true',
    }

    parameters['q'] = q
    if facets:
        parameters['facet_by'] = facets

    response = session.get(SEARCH, params=parameters)

    return response

