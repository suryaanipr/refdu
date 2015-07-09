from django.conf.urls import patterns, include, url
#from django.contrib import admin
#from django.views.generic import TemplateView
#import authentication
from views import *

urlpatterns = patterns('authentication.views',
    url(r'^register$', register),
    url(r'^login$',login),
    url(r'^get_user_data', UserData.as_view()),
    url(r'^logout', logout),
    url(r'^mail', send_activation_link),
    url(r'^activate', activate_link),
    url(r'^send_forgot_link', send_forgot_link),
    url(r'^update_forgot_password', update_forgot_password),
)