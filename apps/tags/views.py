# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from apps.userManager.models import  Profile

import pprint
import json
# Create your views here.

# Crea la lista de envíos predefinida
def loadPredefinedList() :
	predefinedList = []

	predefinedList.append(dict([ ('username','todos'), ('firstName','Todos los usuarios'), ('lastName',''), ('email','') ]))
	predefinedList.append(dict([ ('username','estudiante'), ('firstName','Todos los estudiantes'), ('lastName',''), ('email','') ]))
	predefinedList.append(dict([ ('username','egresado'), ('firstName','Todos los egresados'), ('lastName',''), ('email','') ]))

	for i in range(1, 11) :
		predefinedList.append(dict([ ('username','semestre_' + str(i)), ('firstName','Estudiantes Semestre'), ('lastName', str(i)), ('email','') ]))

	return predefinedList


# Filtra una lista de objetos.
# El objeto se filtra en su atributo firstName según coincidencias con @tag
#
# @param list : lista de objetos con un atributo firstName
# @param tag : cadena de texto a buscar
#
# @return: (list)
def filter_by_tag( list, tag ) :
	found = []
	s = tag.lower()
	for el in list:
		value = el['firstName'].lower()
		if value.find(s) != -1 :
			found.append(el)

	return found


def autocomplete(request,*args):
	key = args[0]
	min_length_for_query = 4
	retorno = {'error':1}

	predefinedList = loadPredefinedList()

	if key == None or len(key) < min_length_for_query :
		return HttpResponse(json.dumps(retorno),content_type="application/json")

	if request.method == 'GET' :

		# Los resultados se inicializan con las coincidencias de la lista
		# de envio predefinida
		results = filter_by_tag(predefinedList, key)

		ob_users= User.objects.none()

		ob_users = User.objects.filter(
			Q(username__startswith=key) |
			Q(first_name__contains=key) |
			Q(last_name__contains=key) |
			Q(email__startswith=key)
		)[:10]


		# Prepare response
		for user in ob_users:
			results.append(dict([
				('username',user.username),
				('firstName',user.first_name),
				("lastName",user.last_name),
				("email",user.email)
			]))

		retorno = {'error':0,'data':results}

		return HttpResponse(json.dumps(retorno),content_type="application/json")

	else:
		return HttpResponse(json.dumps(retorno),content_type="application/json")
