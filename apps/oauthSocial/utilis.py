from apps.oauthSocial.models import App , CuentaSocial , TokenSocial
from twython import Twython
import pprint


def verificar_conexion_twitter(usuario):

	ob_app=App.objects.get_or_none(provedor="Twitter")
	ob_CuentaSocial=CuentaSocial.objects.get_or_none(user=usuario)
	if ob_CuentaSocial :
		ob_TokenSocial=TokenSocial.objects.get_or_none(cuenta=ob_CuentaSocial)
		if ob_TokenSocial:
			twitter  =  Twython ( ob_app.consumer_key ,  ob_app.consumer_secret , ob_TokenSocial.token ,  ob_TokenSocial.token_secreto )
			try:
				twitter.verify_credentials()
			except ValueError:
				return False
			return True		
		else:
			return False
	else :
		return False