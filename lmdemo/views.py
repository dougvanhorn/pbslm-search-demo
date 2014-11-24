# Views for exploring the LM API.
import json
import pygments
import pygments.lexers
import pygments.formatters

from django import http
from django.contrib import messages
from django.shortcuts import render

from . import forms
from . import lmapi
from . import loginbypass


# Utility functions.

def _pygments_json(data):
    """Return an HTML formatted string using Pygments for the given dictionary.

    data -- a dictionary to convert to HTML formatted JSON.
    """
    formatted_json = json.dumps(
        data,
        sort_keys=True,
        separators=(',', ': '),
        indent=4,
    )
    lexer = pygments.lexers.JsonLexer()
    formatter = pygments.formatters.HtmlFormatter(
        linenos=True,
        cssclass='pygments-highlight'
    )
    highlighted_json = pygments.highlight(
        formatted_json,
        lexer,
        formatter,
    )
    return highlighted_json


def homepage(request):
    """Render the homepage.
    """
    t = 'homepage.html'
    d = {}


    if 'query' in request.GET:
        form = forms.SearchForm(request.GET)
        d['form'] = form

        if form.is_valid():
            query = form.cleaned_data.get('query', '')
            grades = form.cleaned_data.get('facet_grades', None)
            language = form.cleaned_data.get('facet_language', None)
            subject = form.cleaned_data.get('facet_subject', None)
            facets = [facet for facet in (grades, language, subject) if facet]
            response = lmapi.search(query, facets=facets)
            d['response'] = response
            data = response.json()
            d['data'] = data
            objects = data['objects']
            d['objects'] = objects
            # Make the formatted JSON avaialable for display.
            d['highlighted_json'] = _pygments_json(data)

            # Can pygments format the json output.
            messages.success(request, "Search successful.")

        else:
            messages.error(request, "Search error.")

    else:
        form = forms.SearchForm()

    return render(request, t, d)


def login_bypass(request):
    """Use PBS Login Bypass to send user to the production website for the
    selected resource.
    """
    lm_url = request.GET.get('url', '/')
    user_id = request.GET.get('user_id', 'lmdemo-271828')
    email = user_id + "@example.com"
    redirect_url = loginbypass.get_redirect(
        url=lm_url,
        user_id=user_id,
        email=email,
        first_name='LMSearchDemo',
        last_name='ExampleUser',
    )

    return http.HttpResponseRedirect(redirect_url)


def standards(request, path=None):
    """Render a navigable Standards Tree.

    User can navigate down through the Standards Tree API endpoint.

    No upward navigation is provided as the API does not provide it.
    """
    template = 'standards.html'
    context = {}

    response = lmapi.standards(path=path)

    # Reponse Data
    context['response'] = response
    data = response.json()
    context['data'] = data
    context['meta'] = data['meta']

    objects = data['objects']
    objects.sort(key=lambda obj: obj['title'])
    # Loop over the objects and modify the Children URL for use in this app.
    # The modified URL Path can be passed directly to this view and to the
    # underlying API call for standards.
    for obj in objects:
        children = obj.get('children', None)
        if children:
            slice_index = children.rfind('standard_tree/')
            obj['children'] = children[slice_index+14:]
    context['objects'] = objects

    # Highlighted JSON
    context['json'] = _pygments_json(data)

    return render(request, template, context)

