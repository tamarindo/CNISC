from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

parceadores_urls = patterns('apps.parceadores.views',

	 url(r'parcearxls/$','parcear_xls', name="parcear_xls"),
)
