from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

tags_urls = patterns('apps.tags.views',
	    url(r'^tags/(\w+)?','autocomplete'),
)
