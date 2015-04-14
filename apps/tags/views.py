from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from apps.userManager.models import  Profile 
import pprint
import json
# Create your views here.


def autocomplete(request,*args):
	pprint.pprint(args)
	if request.method == 'GET' :
		table = 'usuarios'
		key = args[0]

		vec_user=[]
		vec_user_meta_filter=[]

		if table == 'usuarios' :
			profile=Profile.objects.get_or_none(name=key)
			if key == "estudiate" or key == 'engresado':

				est = User.objects.filter(userext__profile=profile)
				for ob_user in est:
					vec_user_meta_filter.append(dict([('username',ob_user.username),('first_name',ob_user.first_name),("last_name",ob_user.last_name),("email",ob_user.email)]))

			ob_users= User.objects.filter(username=key,first_name__contains=key, last_name__contains=key,email__contains=key)
			
			for ob_user in ob_users:
				vec_user.append(dict([('username',ob_user.username),('first_name',ob_user.first_name),("last_name",ob_user.last_name),("email",ob_user.email)]))
			vec_total= list(set(vec_user_meta_filter) | set(vec_user))
			retorno = {'error':0,'data':vec_total}
		else:
			retorno = {'error':1}						
	else:
		retorno = {'error':1}

	return HttpResponse(json.dumps(retorno),content_type="application/json")	