# coding=utf-8
from apps.oauthSocial.models import App , CuentaSocial , TokenSocial
from apps.userManager.models import UserExt,Profile
from twython import Twython
import pprint

# HTTP fetch requests
import urllib
import urllib2


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


# Crea un post en la página de Facebook
# @ref https://developers.facebook.com/docs/graph-api/reference/v2.3/page/feed
def facebook_push( admin, csv_user ) :
	fb_token = get_token_social(admin, 'Facebook')

	if not fb_token or not csv_user :
		pprint.pprint( 'EXCEPTION No hay token o ids de usuario' )
		return False

	# Publish to page endpoint
	url = 'https://graph.facebook.com/v2.3/' + fb_token.cuenta.uid + '/feed'
	data = {}
	data['access_token'] = fb_token.token
	data['message'] = 'Hola! Te han enviado un nuevo mensaje privado.'
	data['tags'] = csv_user
	data['place'] = '106306402741737' # Pereira

	data['link'] = 'http://isc.utp.edu.co/'
	data['picture'] = ''
	data['name'] = 'Centro de Notificaciones ISC'
	data['description'] = 'Ingresa al centro de notificaciones para visualizar el mensaje enviado. Revísalo en CNISC'

	# Create request object
	url_data = urllib.urlencode(data)
	req = urllib2.Request(url, url_data)
	res = urllib2.urlopen(req)

	# @TODO: Guardar el ID retornado por Facebook en el log del sistema
	pprint.pprint(res.read())


def get_name_tw_admin():
	ob_profile= Profile.objects.get_or_none(is_admin=True)
	ob_u= UserExt.objects.get_or_none(profile=ob_profile)
	ob_Cs=CuentaSocial.objects.get_or_none(user=ob_u.user,app__provedor='Twitter')
	return ob_Cs.screen_name
