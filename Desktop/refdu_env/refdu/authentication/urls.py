from django.conf.urls import patterns, include, url
#from django.contrib import admin
#from django.views.generic import TemplateView
#import authentication
from views import *

urlpatterns = patterns('authentication.views',
    url(r'^register$', register),
    url(r'^login$',login),
    url(r'^get_user_data', UserData.as_view()),
    url(r'^test', testing_on_token),
)