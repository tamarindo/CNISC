from django.core.validators import validate_email
from django.contrib.auth.models import User
from pprint import pprint
from apps.main.utils import send_email
import json

def notificarMensaje(json_recipients):
	array = []
	json_recipients=json.loads(json_recipients)
	for data_id in json_recipients['users']:
		pprint(int(data_id))
		ob_user= User.objects.get(username=int(data_id))
		if ob_user.userext.email_alt != None:
			array.append(ob_user.userext.email_alt)
		else:
			array.append(ob_user.email)
	email_context = {
					'key'    : p,
			        'titulo' : 'Recuperación de password',
			        # FIXME costruir tambien el nombre del dominio (host)
			        'url'    : request.META['HTTP_HOST'] + reverse('verificar_keys'), 
			        'usuario': ob_user[0].get_full_name(),
			    }
	send_email(email_context,'email_keys_send.html','Recupera Password CNISC','no-reply@isc.edu.co',[email]);



	return False