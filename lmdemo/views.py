# Views for exploring the LM API.
import datetime
import hashlib
import json
import pygments
import pygments.lexers
import pygments.formatters
import random

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


def login_bypass_error(request):
    """Show the Error response from the API.
    """
    return http.HttpResponse(request.session.get('login_bypass_error'))


def login_bypass_form(request):
    template = 'login-bypass.html'
    context = {}

    if request.method == 'GET':
        today = datetime.date.today()
        random_string = hashlib.md5(bytes(str(random.random()).encode('utf-8'))).hexdigest()
        user_id = today.strftime('lmdemo-%y%m%d-')
        user_id += random_string[:3]

        initial_form = {
            'lm_url': '/',
            'first_name': 'Test',
            'last_name': 'Example',
            'user_id': user_id,
            'email': '{}@example.com'.format(user_id),
            'postal_code': '63303',
        }
        form = forms.LoginBypassForm(initial=initial_form)
        context['form'] = form
        return render(request, template, context)

    else:
        form = forms.LoginBypassForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                redirect_url = loginbypass.get_redirect(
                    url=cleaned_data.get('lm_url'),
                    user_id=cleaned_data.get('user_id'),
                    email=cleaned_data.get('email'),
                    first_name=cleaned_data.get('first_name'),
                    last_name=cleaned_data.get('last_name'),
                    postal_code=cleaned_data.get('postal_code'),
                )
                return http.HttpResponseRedirect(redirect_url)
            
            except loginbypass.LoginBypassError as e:
                request.session['login_bypass_error'] = e.response.text
                context['login_bypass_error'] = e

        context['form'] = form
        return render(request, template, context)
        

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

    # Highlighted JSON
    context['json'] = _pygments_json(data)

    objects = data['objects']
    objects.sort(key=lambda obj: obj['title'])

    # Loop over the objects and modify the Children URL for use in this app.
    # The modified URL Path can be passed directly to this view and to the
    # underlying API call for standards.
    # E.g., takes a string like:
    #    http://www.pbslearningmedia.org/api/v2/standard_tree/12/40/
    # and turns it into:
    #    12/40/
    for obj in objects:
        children = obj.get('children', None)
        if children:
            slice_index = children.rfind('standard_tree/')
            obj['children'] = children[slice_index+14:]
    context['objects'] = objects

    return render(request, template, context)


def subjects(request, path=None):
    """Render a navigable Subjects Tree.

    User can navigate down through the Subjects Tree API endpoint.

    No upward navigation is provided as the API does not provide it.
    """
    template = 'subjects.html'
    context = {}

    response = lmapi.subjects(path=path)

    # Reponse Data
    context['response'] = response
    data = response.json()
    context['data'] = data
    context['meta'] = data['meta']

    # Highlighted JSON
    context['json'] = _pygments_json(data)

    objects = data['objects']
    objects.sort(key=lambda obj: obj['title'])

    # Loop over the objects and modify the Children URL for use in this app.
    # The modified URL Path can be passed directly to this view and to the
    # underlying API call for standards.
    # E.g., takes a string like:
    #    http://www.pbslearningmedia.org/api/v2/subject_tree/282/
    # and turns it into:
    #    282/
    for obj in objects:
        children = obj.get('children', None)
        if children:
            slice_index = children.rfind('subject_tree/')
            obj['children'] = children[slice_index+13:]
    context['objects'] = objects

    return render(request, template, context)

