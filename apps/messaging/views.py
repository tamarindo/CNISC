from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
from django.views.generic import View

from apps.messaging.models import View_Messages_User , Message
from apps.messaging.utils import notificarMensaje

import pprint
import json
# Create your views here.
# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------

class Mensajes(View):

	http_method_names = ['get','put','post']

	def get(self,request,*args,**kwargs):
		if args == () :	 
			#Enviar Varios Mensajes en base a los parametros
			ob_user=User.objects.get(id=request.user.id)
			lim_inf = int( request.GET.get('offset') ) + 1
			private=request.GET.get('private')
			lim_sup = lim_inf + 10

			if lim_inf and lim_sup and private:
				if int(private):
					vector_view_message_private  = []
					list_view_message_private = View_Messages_User.objects.filter(user=ob_user,private = True ).order_by('date_added')[lim_inf:lim_sup]
					
					for item_view_message in list_view_message_private:
						vector_view_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
					
					retorno = vector_view_message_private

				else:
					vector_view_message_no_private = []
					list_view_message_no_private = View_Messages_User.objects.filter(user=ob_user ,private = False).order_by('date_added')[lim_inf:lim_sup]
					
					for item_view_message in list_view_message_no_private:
						vector_view_message_no_private.append(
						dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
					
					retorno = vector_view_message_no_private
			else:
				retorno = {'error':1,'msj':'Faltan parametros'}

			return HttpResponse(json.dumps(retorno),content_type="application/json")

		else:
			#Enviar un solo Mensaje
			mensaje_id = int( args[0] )
			ob_user=User.objects.get(id=request.user.id)

			vector_view_messag= []
			ob_view_message = View_Messages_User.objects.get( pk = mensaje_id )
			retorno = dict([('id',ob_view_message.id),('asunto',ob_view_message.message.subject),('mensaje',ob_view_message.message.content), ('esvisto',ob_view_message.seen), ('fecha',ob_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))])

			return HttpResponse(json.dumps(retorno),content_type="application/json")


	def put(self,request,*args,**kwargs):

		#Pasar a estado leido un mensaje

		if args != () :
			if type(args[0]) != int :								
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
			else:
				retorno = {'error':1,'msj':'peticion erronea'}

			return HttpResponse(json.dumps(retorno),content_type="application/json")
		else :

			id_user = request.user.id
			ob_viewmessage = View_Messages_User.objects.filter(user=id_user).update(seen=True)
			retorno = {'error':0}
			return HttpResponse(json.dumps(retorno),content_type="application/json")


	def post(self,request,*args,**kwargs):

		#Crear Mensaje
		
		subject=request.POST.get('subject')
		json_recipients=request.POST.get('json_recipients')
		content_men=request.POST.get('content_men')
		private=request.POST.get('private') 
		
		if private == None :
			private = False 

		if subject and json_recipients and content_men:

			new_mensaje= Message(sender=request.user,subject=subject,content=content_men)
			new_mensaje.save()
			recipients=json.loads(json_recipients)
			for receiver in recipients['users']:
				ob_user = User.objects.get(username=int(receiver))
				if ob_user:
					pass
					#newView=View_Messages_User(message=new_mensaje,user=ob_user,private=private)
					#newView.save()
			
			notificarMensaje(json_recipients)
			
			retorno = {'error':0,'msj':' '}

		else:
			retorno = {'error':1,'msj':'Faltan parametros'}

		return HttpResponse(json.dumps(retorno),content_type="application/json")



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



	

	
