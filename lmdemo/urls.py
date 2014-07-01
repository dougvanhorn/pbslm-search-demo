from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import lmdemo.views

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', lmdemo.views.homepage, name="homepage"),
)
