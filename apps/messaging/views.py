from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User

from apps.messaging.models import View_Messages_User

import pprint
import json
# Create your views here.
# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------

def getMessage(request):
	ob_user=User.objects.get(id=request.user.id)
	lim_inf=request.POST.get('lim_inf')
	lim_sup=request.POST.get('lim_sup')
	
	if lim_inf and lim_sup:
		vector_view_message=[]
		list_view_message=View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup ).order_by('date_added')
		for item_view_message in list_view_message:
			vector_view_message.append(
			dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))])
			)
		retorno = vector_view_message
	else:
		retorno = {'error':1,'msj':'Faltan parametros'}
	
	return HttpResponse(json.dumps(retorno),content_type="application/json")


def seenMessage(request):
	id_viewmessage=request.POST.get('id')
	ob_viewmessage=View_Messages_User.objects.get_or_none(id=id_viewmessage)
	
	if ob_viewmessage:
		if ob_viewmessage.seen != True:
			ob_viewmessage.seen = True
			try:
				ob_viewmessage.save()
				retorno = {'error':0}
			except:
				retorno = {'error':1,'msj':'error al guardar'}
		else:
			retorno = {'error':0}	
	else:
		retorno = {'error':1,'msj':'Mensaje inexistente'}

	return HttpResponse(json.dumps(retorno),content_type="application/json")


	

def seenAllMessage(request):
	id_user = request.user.id
	ob_viewmessage = View_Messages_User.objects.filter(user=id_user).update(seen=True)
	return HttpResponse(json.dumps({'error':0}),content_type="application/json")




	
# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------