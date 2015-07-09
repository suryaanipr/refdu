from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from authentication import urls

urlpatterns = patterns('authentication.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^auth/', include(urls)),

)