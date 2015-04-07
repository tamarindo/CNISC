from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


from .views import  Email 


admin.autodiscover()

userManager_urls = patterns('apps.userManager.views',
	# urls de login
    url(r'^logout$', 'v_logout', name="v_logout"),
    url(r'^login/$','login', name="login"),
    url(r'^login/password_reset/$','recuperar_pass', name="recuperar_pass"),
    url(r'^login/new_password/(\w+)?','verificar_keys', name="verificar_keys"),
    # url api V2 
    url(r'^api/avisos/bienvenida$', 'aviso_bienvenida',name='aviso_bienvenida'),
    url(r'^api/usuario/correo/', Email.as_view()),
    url(r'^api/userManager/cambiar_foto$', 'change_foto', name="change_foto"),
    url(r'^api/userManager/eliminar_foto$', 'eliminar_foto', name="eliminar_foto"),
    url(r'^api/userManager/cambiar_correo$', 'changeemail', name="changeemail"),


)
