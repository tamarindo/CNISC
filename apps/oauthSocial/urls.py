from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

oauthSocial_urls = patterns('apps.oauthSocial.views',
	url(r'^autentificar_twitter$','autentificar_usuario_twitter',name="autentificar_twitter"),
	url(r'^callback_twitter$','callbacktwitter',name="callbacktwitter"),
	
)     
  


