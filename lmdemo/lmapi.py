"""Library to use the Search API.
"""

import requests

from django.conf import settings


SEARCH = "{}/search/".format(settings.LMAPI_URI)
LO = "{}/lo/".format(settings.LMAPI_URI)
STANDARDS = "{}/standard_tree/".format(settings.LMAPI_URI)
SUBJECTS = "{}/subject_tree/".format(settings.LMAPI_URI)


AUTHORIZATION = {'Authorization': 'ApiKey {}:{}'.format(
    settings.LMAPI_USERNAME,
    settings.LMAPI_APIKEY,
)}


"""API Feedback:

copywright is spelled wrong.

Do we want to show the media_urls?
"""

class LMAPIException(Exception):
    pass


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


def standards(path=''):
    """Return the Standards response for the given path.
    Arguments:
        path: an ID path to use in the query, from the children URL.

    Returns:
        A `requests.Response` instance.
    """
    standard_uri = "{}{}".format(STANDARDS, path)

    session = get_session()
    response = session.get(standard_uri)

    if response.status_code != 200:
        raise LMAPIException()

    return response


def subjects(path=''):
    """Return the subjects response for the given path.
    Arguments:
        path: an ID path to use in the query, from the children URL.

    Returns:
        A `requests.Response` instance.
    """
    standard_uri = "{}{}".format(SUBJECTS, path)

    session = get_session()
    response = session.get(standard_uri)

    if response.status_code != 200:
        raise LMAPIException()

    return response

