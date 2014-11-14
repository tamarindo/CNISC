from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout


from twython import Twython


def autentificar_usuario_twitter(request):

	ob_app=App.object.get(provedor="Twitter")
	APP_KEY = ob_app.consumer_key
	APP_SECRET = ob_app.consumer_secret

	ob_cuenta_twitter=CuentaSocial.object.get_or_none(user=request.user)
	twitter = Twython(APP_KEY, APP_SECRET)
	auth = twitter.get_authentication_tokens(callback_url='localhost:8000/callback')	
	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']



	if !ob_cuenta_twitter:
		new_cuenta_twitter = CuentaSocial(user=request.user,select=1,app=ob_app)
		new_cuenta_twitter.save()
		token_social = TokenSocial(cuenta=new_cuenta_twitter,token=OAUTH_TOKEN,token_secreto=OAUTH_TOKEN_SECRET)
		token_social.save()
	
	else :
		ob_token = TokenSocial.object.get_or_none(cuenta=ob_cuenta_twitter)

		if !ob_token :
		ob_token.token(OAUTH_TOKEN)
		ob_token.token_secreto(OAUTH_TOKEN_SECRET)
		ob_token.save()

		else:  
		token_social = TokenSocial(cuenta=cuenta_twitter,token=OAUTH_TOKEN,token_secreto=OAUTH_TOKEN_SECRET)
		token_social.save()

    return HttpResponseRedirect(auth['auth_url'])


def callbacktwitter(request):

	ob_app=App.object.get(provedor="Twitter")
	ob_cuenta_twitter=CuentaSocial.object.get_or_none(user=request.user)
	ob_token = TokenSocial.object.get_or_none(cuenta=ob_cuenta_twitter)	
	
	if  ob_app and ob_cuenta_twitter and ob_token :

		oauth_verifier=request.GET.get('oauth_verifier')
		twitter = Twython(ob_app.consumer_key, ob_app.consumer_secret,ob_token.token, ob_token.token_secreto)
		final_step = twitter.get_authorized_tokens(oauth_verifier)
		ob_token.token = final_step['oauth_token']
		ob_token.token_secreto =  final_step['oauth_token_secret']
	
	return HttpResponseRedirect(reverse("preferences"))	

