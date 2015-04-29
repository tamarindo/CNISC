from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from apps.userManager.models import  Profile 

import pprint
import json
# Create your views here.


def autocomplete(request,*args):
	key = args[0]
	min_length_for_query = 4
	retorno = {'error':1}

	pprint.pprint(key)
	
	if key == None or len(key) < min_length_for_query :
		return HttpResponse(json.dumps(retorno),content_type="application/json")

	if request.method == 'GET' :

		vec_user=[]
		ob_users= User.objects.none()

		ob_users = User.objects.filter(
			Q(username__startswith=key) | 
			Q(first_name__contains=key) | 
			Q(last_name__contains=key) | 
			Q(email__startswith=key)
		)[:10]


		# Prepare response
		for user in ob_users:
			vec_user.append(dict([
				('username',user.username),
				('firstName',user.first_name),
				("lastName",user.last_name),
				("email",user.email)
			]))
		
		retorno = {'error':0,'data':vec_user}

		return HttpResponse(json.dumps(retorno),content_type="application/json")	

	else:
		return HttpResponse(json.dumps(retorno),content_type="application/json")
