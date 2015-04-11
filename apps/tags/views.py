from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

import pprint
import json
# Create your views here.


def autocomplete(request,*args):
	pprint.pprint(args)
	if request.method == 'GET' :
		table = 'usuarios'
		key = args

		vec_user=[]
		vec_user_user=[]
		vec_user_enge=[]
		est = [] 
		eng = []

		if table == 'usuarios' :
			if key == "estudiate":
				est = User.objects.filter(userext__profile__name=key)
				for ob_user in est:
					vec_user_user.appent(dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email)]))

			elif key == 'engresado':
				eng = User.objects.filter(userext__profile__name=key)
				for ob_user in eng:
					vec_user_enge.appent(dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email)]))

			ob_users= User.objects.filter(username=key,fist_name__contains=key, last_name__contains=key,email__contains=key)
			
			for ob_user in ob_users:
				vec_useSr.appent(dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email)]))
			vec_total= vec_user_enge | vec_user_enge | vec_user
			retorno = {'error':0}
		else:
			retorno = {'error':1}						
	else:
		retorno = {'error':1}

	return HttpResponse(json.dumps(retorno),content_type="application/json")	