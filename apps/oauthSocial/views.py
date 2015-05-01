from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from apps.oauthSocial.models import App , CuentaSocial , TokenSocial
from apps.oauthSocial.forms import editApp
from apps.oauthSocial.utilis import *
from twython import Twython
from django.contrib.auth.models import User

import pprint, json, datetime

 # configurar las aplicaciones externas

def configura_app(request, *args):
	provedor= args[0]
	pprint.pprint(provedor)
	if provedor == "Facebook" or provedor == "Twitter": 
		if request.method == 'POST':
	 		modelsfrom = editApp(request.POST)
	 		if modelsfrom.is_valid():
	 			modelsfrom.save()
	 			mensaje=" Aplicacion Guardada "	
	 			error=1
	 		else :
	 			mensaje=" Error al guardar "
	 			error=0
	 		return render_to_response('templateFormularioApp.html',{'formulario':modelsfrom,'error':error,'mensaje':mensaje},context_instance=RequestContext(request))
		else:
			ob_app= App.objects.get_or_none(provedor=provedor)
			pprint.pprint(ob_app)
			if ob_app:
				modelsfrom = editApp(instance=ob_app)
				return render_to_response('templateFormularioApp.html',{'formulario':modelsfrom},context_instance=RequestContext(request))				
			else:
	 			return HttpResponseRedirect(reverse("preferences"))	
	else:
		return HttpResponseRedirect(reverse("preferences"))	
	

# metodos para tw
def callbacktwitter(request):
	pprint.pprint(request.user)
	ob_app=App.objects.get_or_none(provedor="Twitter")
	ob_user = User.objects.get(pk=request.user.pk)
	ob_cuenta_twitter=CuentaSocial.objects.get(user=ob_user)


	if ob_cuenta_twitter != None:
		ob_token = TokenSocial.objects.get_or_none(cuenta=ob_cuenta_twitter)		
		oauth_verifier=request.GET.get('oauth_verifier')

	if  ob_app and ob_cuenta_twitter and ob_token and oauth_verifier:
		twitter = Twython(ob_app.consumer_key, ob_app.consumer_secret,ob_token.token, ob_token.token_secreto)
		final_step = twitter.get_authorized_tokens(oauth_verifier)
		ob_token.token = final_step['oauth_token']
		ob_token.token_secreto =  final_step['oauth_token_secret']
		ob_cuenta_twitter.screen_name =  final_step['screen_name']
		ob_cuenta_twitter.uid =final_step['user_id']
		ob_cuenta_twitter.save()
		ob_token.save()

		return HttpResponseRedirect(reverse("preferences"))	



def autentificar_usuario_twitter(request):
		ob_app=App.objects.get(provedor="Twitter")
		APP_KEY = ob_app.consumer_key
		APP_SECRET = ob_app.consumer_secret

		ob_cuenta_twitter=CuentaSocial.objects.get_or_none(user=request.user)
		twitter = Twython(APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/api/oauth/callback_twitter')	
		OAUTH_TOKEN = auth['oauth_token']
		OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

		if  not ob_cuenta_twitter:
			new_cuenta_twitter = CuentaSocial(user=request.user,select=1,app=ob_app)
			new_cuenta_twitter.save()
			token_social = TokenSocial(cuenta=new_cuenta_twitter,token=OAUTH_TOKEN,token_secreto=OAUTH_TOKEN_SECRET)
			token_social.save()
		
		else :
			ob_token = TokenSocial.objects.get_or_none(cuenta=ob_cuenta_twitter)
			if  ob_token :

				ob_token.token=OAUTH_TOKEN
				ob_token.token_secreto=OAUTH_TOKEN_SECRET
				ob_token.save()

			else:  
				token_social = TokenSocial(cuenta=ob_cuenta_twitter,token=OAUTH_TOKEN,token_secreto=OAUTH_TOKEN_SECRET)
				token_social.save()

		return HttpResponseRedirect(auth['auth_url'])


# metodos para fb
def facebook_connect(request):

	if 'POST' != request.method :
		return HttpResponseRedirect( reverse("home") )

	ob_app = App.objects.get_or_none(provedor="Facebook")
	ob_user = User.objects.get(pk=request.user.pk)

	access_token = request.POST.get('accessToken')
	uid = request.POST.get('userID')
	delta = int(request.POST.get('expiresIn'))
	expires_in = datetime.datetime.utcnow() + datetime.timedelta(seconds=delta)

	# Cuenta Social
	# Se actualiza o crea el usuario si es que ya existe para esta app
	ob_cuenta_social = CuentaSocial.objects.update_or_create(user=ob_user, app=ob_app, defaults={'uid': uid})
	pprint.pprint(ob_cuenta_social)
	
	# Tokens
	TokenSocial.objects.update_or_create(cuenta=ob_cuenta_social[0], defaults={'token':access_token, 'token_secreto':access_token, 'fecha_expiracion':expires_in })

	return HttpResponse( json.dumps({'error': 0, 'message': ''}), content_type='application/json' )
