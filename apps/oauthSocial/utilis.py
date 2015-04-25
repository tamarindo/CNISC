from apps.oauthSocial.models import App , CuentaSocial , TokenSocial
from apps.userManager.models import UserExt,Profile
from twython import Twython
import pprint


def get_token_social(usuario, proveedor) :
	ob_app = App.objects.get_or_none(provedor=proveedor)
	ob_CuentaSocial = CuentaSocial.objects.get_or_none(user=usuario, app=ob_app)
	
	if ob_CuentaSocial :
		return TokenSocial.objects.get_or_none(cuenta=ob_CuentaSocial)

	return None


def verificar_conexion_twitter(usuario) :
	ob_TokenSocial = get_token_social(usuario, 'Twitter')
	ob_app=App.objects.get_or_none(provedor="Twitter")	
	if ob_TokenSocial:
		twitter  =  Twython ( ob_app.consumer_key ,  ob_app.consumer_secret , ob_TokenSocial.token ,  ob_TokenSocial.token_secreto )
		try:
			twitter.verify_credentials()
		except ValueError:
			return False
		return True		
	else:
		return False

def conexion_twitter(usuario) :
	ob_TokenSocial = get_token_social(usuario, 'Twitter')
	ob_app=App.objects.get_or_none(provedor="Twitter")
	if ob_TokenSocial:
		twitter  =  Twython ( ob_app.consumer_key ,  ob_app.consumer_secret , ob_TokenSocial.token ,  ob_TokenSocial.token_secreto )
		try:
			twitter.verify_credentials()
		except ValueError:
			return False
		return twitter		
	else:
		return False



def verificar_conexion_facebook(usuario) :
	ob_token_social = get_token_social(usuario, 'Facebook')

	if not ob_token_social :
		return False

	return True


def get_name_tw_admin():
	ob_profile= Profile.objects.get_or_none(is_admin=True)
	ob_u= UserExt.objects.get_or_none(profile=ob_profile)
	ob_Cs=CuentaSocial.objects.get_or_none(user=ob_u.user,app__provedor='Twitter')
	return ob_Cs.screen_name