from django.shortcuts import render
from django.contrib.auth.models import User

import pprint
import json
# Create your views here.


def autocomplete(request):

	if request.method == 'GET' :
		table = request.GET.get('table')
		key = request.GET.get('key')		
		if table == 'usuarios' :
			ob_users= user.objects.filter(username=key,fist_name__contains=key, last_name__contains=key,email__contains=key)
			vec_user=[]
			for ob_user in ob_users:
				vec_user.appent(dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email)]))
			retorno = {'error':0}						
	else:
		retorno = {'error':1,'msj':'Error en methodo de envio'}

	return HttpResponse(json.dumps(retorno),content_type="application/json")	