from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from apps.messaging.views import Mensajes


admin.autodiscover()

messaging_urls = patterns('apps.messaging.views',

	url(r'^mensajes/(\d+)', Mensajes.as_view()),
	url(r'^mensajes', Mensajes.as_view()),

#  estos metodos se les tiene que dejar de dar soporte
	url(r'^marcar_todo_como_leido$', 'seenAllMessage', name="seenAllMessage"),
    url(r'^marcar_como_leido$', 'seenMessage', name="seenMessage"),
    url(r'^recargar_msj$', 'getMessage', name="getMessage"),
#  ..
)
