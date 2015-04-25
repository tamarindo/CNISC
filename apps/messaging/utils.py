from django.contrib.auth.models import User
from pprint import pprint
from apps.main.utilities import send_email
from django.core.mail.message import EmailMultiAlternatives
from apps.main.utilities import *
from apps.oauthSocial.utilis import *
from pprint import pprint
import json

def notificar_mensaje(json_recipients,asunto,contenido,admin_user):
	array = []
	json_recipients=json.loads(json_recipients)
	

	
	for data_id in json_recipients['users']:

		ob_user= User.objects.get(username=int(data_id))
		if ob_user :	
			if ValidateEmail(ob_user.userext.email_alt):
				array.append(ob_user.userext.email_alt)
			elif ValidateEmail(ob_user.email):
				array.append(ob_user.email)

		ob_cs=CuentaSocial.objects.get_or_none(user=ob_user)
		cursor_tw = conexion_twitter(admin_user)
		if cursor_tw :

			texto = "@"+ob_cs.screen_name+" hola tienes un nuevo mensaje privado en Centro de mensajes ISC - UTP  Sigue el link "
			# TODO Manejar excepcion para informar al usuario que tiene que segir a la cuenta del admin
			try:
				cursor_tw.update_status(status= texto )
			except Exception, e:
				pass
	
	correo = EmailMultiAlternatives(asunto,contenido,'no-reply@isc.edu.co',array)
	correo.attach_alternative(contenido, 'text/html')
	correo.send()



	return False