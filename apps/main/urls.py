from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from .views import  Usuario 
admin.autodiscover()

main_urls = patterns('apps.main.views',
	
	url(r'^api/main/configuracion_visualizacion$', 'changeTypeVisualization', name="changeTypeVisualization"),
		# url Templates
    url(r'^$','home', name="home"),
	url(r'^preferencias$','preferences',name="preferences"),

	url(r'^usuarios$','panelUseradmin',name="panelUseradmin"),
    url(r'^usuario/editar/(\d+)', Usuario.as_view() ,name="usereditaradmin"),


)