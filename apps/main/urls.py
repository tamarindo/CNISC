from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

main_urls = patterns('apps.main.views',
    url(r'home','home', name="home"),   
)  


