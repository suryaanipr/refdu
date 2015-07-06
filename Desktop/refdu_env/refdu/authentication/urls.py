from django.conf.urls import patterns, include, url
#from django.contrib import admin
#from django.views.generic import TemplateView
#import authentication
from views import *

urlpatterns = patterns('authentication.views',
    url(r'^register$', Register.as_view()),
)