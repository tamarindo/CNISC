from django.core.validators import validate_email
from django.contrib.auth.models import User
from pprint import pprint
from apps.main.utilities import send_email
from django.core.mail.message import EmailMultiAlternatives

import json

def notificarMensaje(json_recipients,asunto,contenido):
	array = []
	json_recipients=json.loads(json_recipients)
	for data_id in json_recipients['users']:
		ob_user= User.objects.get(username=int(data_id))
		if ob_user.userext.email_alt != None:
			array.append(ob_user.userext.email_alt)
		else:
			array.append(ob_user.email)

	correo = EmailMultiAlternatives(asunto,contenido,'no-reply@isc.edu.co',array)
	correo.attach_alternative(contenido, 'text/html')
	correo.send()



	return False