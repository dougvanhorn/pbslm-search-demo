from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import lmdemo.views

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', lmdemo.views.homepage, name="homepage"),

    url(r'^standards/(?P<path>.*)$', lmdemo.views.standards, name="standards"),

    url(r'^login-bypass$',
        lmdemo.views.login_bypass,
        name="login_bypass"),
)
