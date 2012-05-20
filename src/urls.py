#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout

# Enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url('^$', 'home.views.index'),
    url('^register/$', 'user_profile.views.register'),
    url('^register_success/$', 'user_profile.views.register_success'),
    url('^login/$', login, {'template_name':"login.html"}),
    url('^logout/$', logout, {'template_name':"logout.html"}),

    url('^my_profile/$', 'user_profile.views.my_profile'),

    url('^sports/$', 'home.views.sports'),
    url('^sports/(?P<sport_id>\d+)/$', 'home.views.sports'),

    url('^tournaments/$', 'home.views.tournaments'),
    url('^tournaments/(?P<tournament_id>\d+)/$', 'home.views.view_fixtures'),
    url('^tournaments/(?P<tournament_id>\d+)/fixtures/$', 'home.views.view_fixtures'),
    #url('^tournaments/(?P<tournament_id>\d+)/new_fixtures/$', 'home.views.view_fixtures_new'),
    url('^tournaments/(?P<tournament_id>\d+)/table/$', 'home.views.view_table'),
    url('^tournaments/(?P<tournament_id>\d+)/predictions/(?P<user_id>\d+)/$', 'home.views.view_user_predictions'),
)
