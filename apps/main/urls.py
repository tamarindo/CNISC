from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

main_urls = patterns('apps.main.views',
	
	url(r'^api/main/configuracion_visualizacion$', 'changeTypeVisualization', name="changeTypeVisualization"),
		# url Templates
    url(r'^$','home', name="home"),
	url(r'^preferencias$','preferences',name="preferences"),
	url(r'^user$','panelUser',name="panelUser"),
	url(r'^users$','panelUseradmin',name="panelUseradmin"),
)