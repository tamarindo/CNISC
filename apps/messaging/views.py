from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
from django.views.generic import View

from apps.messaging.models import View_Messages_User

import pprint
import json
# Create your views here.
# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------

class Mensajes(View):

	http_method_names = ['get','pull','post']

	def get(self,request,*args,**kwargs):
		pprint.pprint(args)
		if args == () :

			#Enviar Varios Mensajes en base a los parametros

			ob_user=User.objects.get(id=request.user.id)
			lim_inf=request.POST.get('lim_inf')
			lim_sup=50
			private=request.POST.get('private')	

			if lim_inf and lim_sup and private:

				if private:
					vector_view_message_private  = []			
					list_view_message_private = View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup,private = True ).order_by('date_added')

					for item_view_message in list_view_message_private:
						vector_view_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
					retorno = vector_view_message_private
				
				else:
					vector_view_message_no_private = []
					list_view_message_no_private = View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup,private = False).order_by('date_added')

					for item_view_message in list_view_message_no_private:
						vector_view_message_no_private.append(
						dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
					retorno = vector_view_message_no_private   
			else:
				retorno = {'error':1,'msj':'Faltan parametros'}
			
			return HttpResponse(json.dumps(retorno),content_type="application/json")

		else:
			#Enviar un solo Mensaje
			pprint.pprint(args[0]) 
			ob_user=User.objects.get(id=request.user.id)

			vector_view_messag= []
			ob_view_message = View_Messages_User.objects.get(pk=args[0])
			retorno = dict([('id',ob_view_message.id),('asunto',ob_view_message.message.subject),('mensaje',ob_view_message.message.content), ('esvisto',ob_view_message.seen), ('fecha',ob_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))])   
			 
			return HttpResponse(json.dumps(retorno),content_type="application/json")	


	def pull(self,request,*args,**kwargs):

		#Pasar a estado leido un mensaje

		if args != () :								
   			id_viewmessage=args[0]
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

			return Response(retorno)
		else :
			id_user = request.user.id
			ob_viewmessage = View_Messages_User.objects.filter(user=id_user).update(seen=True)
			retorno = {'error':0}
			return Response(retorno)


# Api Vieja	  Despues de Provar la nueva api se pude eliminar


def getMessage(request):
	ob_user=User.objects.get(id=request.user.id)
	lim_inf=request.POST.get('lim_inf')
	lim_sup=request.POST.get('lim_sup')
	private=request.POST.get('private')	

	if lim_inf and lim_sup and private:

		if private:
			vector_view_message_private  = []			
			list_view_message_private = View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup,private = True ).order_by('date_added')

			for item_view_message in list_view_message_private:
				vector_view_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
			retorno = vector_view_message_private
		
		else:
			vector_view_message_no_private = []
			list_view_message_no_private = View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup,private = False).order_by('date_added')

			for item_view_message in list_view_message_no_private:
				vector_view_message_no_private.append(
				dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
			retorno = vector_view_message_no_private   
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



	

	
