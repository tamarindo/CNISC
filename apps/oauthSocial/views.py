from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from apps.oauthSocial.models import App , CuentaSocial , TokenSocial

from twython import Twython

import pprint

def callbacktwitter(request):
	ob_app=App.objects.get_or_none(provedor="Twitter")

	ob_cuenta_twitter=CuentaSocial.objects.get(user=request.user)

	pprint.pprint(ob_cuenta_twitter)
	if ob_cuenta_twitter != None:
		ob_token = TokenSocial.objects.get_or_none(cuenta=ob_cuenta_twitter)		
		oauth_verifier=request.GET.get('oauth_verifier')


	if  ob_app and ob_cuenta_twitter and ob_token and oauth_verifier:
	
		pprint.pprint(oauth_verifier)			

		twitter = Twython(ob_app.consumer_key, ob_app.consumer_secret,ob_token.token, ob_token.token_secreto)
		final_step = twitter.get_authorized_tokens(oauth_verifier)
		pprint.pprint(final_step)
		ob_token.token = final_step['oauth_token']
		ob_token.token_secreto =  final_step['oauth_token_secret']

		ob_cuenta_twitter.uid =final_step['user_id']
		pprint.pprint(ob_cuenta_twitter.uid)
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



