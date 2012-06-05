#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset

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

    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/', "template_name":"password_reset_form.html"}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', 
        {"template_name":"password_reset_done.html"}),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/', 'template_name': 'password_reset_confirm.html'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete', {"template_name": "password_reset_complete.html"}),


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
