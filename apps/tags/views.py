from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from apps.userManager.models import  Profile 
import pprint
import json
# Create your views here.


def autocomplete(request,*args):
	if request.method == 'GET' :
		table = 'usuarios'
		key = args[0]

		vec_user=[]
		ob_users= User.objects.none()
		tags_user= User.objects.none()
		
		if table == 'usuarios' :
			profile=Profile.objects.get_or_none(name=key)
			if key == "estudiante" or key == 'engresado':
				pprint.pprint(key)
				tags_user = User.objects.filter(userext__profile=profile)	
			ob_users= User.objects.filter(username=key,first_name__contains=key, last_name__contains=key,email__contains=key)
			union_user= ob_users | tags_user
			pprint.pprint(ob_users)
			pprint.pprint(tags_user)
			for ob_user in union_user:
				vec_user.append(dict([('username',ob_user.username),('first_name',ob_user.first_name),("last_name",ob_user.last_name),("email",ob_user.email)]))
			
			retorno = {'error':0,'data':vec_user}
		else:
			retorno = {'error':1}						
	else:
		retorno = {'error':1}

	return HttpResponse(json.dumps(retorno),content_type="application/json")	