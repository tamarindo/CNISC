from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


from .views import  Usuario , Email 


admin.autodiscover()

userManager_urls = patterns('apps.userManager.views',
	# urls de login
    url(r'^logout$', 'v_logout', name="v_logout"),
    url(r'^login/$','login', name="login"),

    # url api V2 
    url(r'^api/usuario/correo/', Email.as_view()),
    url(r'^usuario/(\d+)', Usuario.as_view()),

	# url api V1
    url(r'^api/userManager/cambiar_correo$', 'changeemail', name="changeemail"),
)
