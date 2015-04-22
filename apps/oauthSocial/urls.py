from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

oauthSocial_urls = patterns('apps.oauthSocial.views',
	url(r'^autentificar_twitter$','autentificar_usuario_twitter',name="autentificar_twitter"),
	url(r'^callback_twitter$','callbacktwitter',name="callbacktwitter"),
	url(r'^configurar_app/(\w+)/$','configura_app',name="configura_app"),

	# Facebook
	url(r'^facebook_connect/$','facebook_connect',name="facebook_connect"),
	
)     
  


