from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

main_urls = patterns('apps.main.views',
	url(r'^apis/main/configuracion_visualizacion$', 'changeTypeVisualization', name="changeTypeVisualization"),
#	url(r'^marcar_todo_como_leido$', 'seenAllMessage', name="seenAllMessage"),
#    url(r'^marcar_como_leido$', 'seenMessage', name="seenMessage"),
#    url(r'^recargar_msj$', 'getMessage', name="getMessage"),
	url(r'^preferencias$','preferences',name="preferences"),

		# url Templates
    url(r'^$','home', name="home"),
)
