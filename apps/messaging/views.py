# coding=utf-8
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.html import strip_tags

from apps.messaging.forms import fromAttachment
from apps.messaging.models import View_Messages_User , Message
from apps.messaging.utils import notificar_mensaje
import sys

from pprint import pprint
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
					list_view_message_private = View_Messages_User.objects.filter(user=ob_user,private = True ).order_by('-date_added')[lim_inf:lim_sup]

					for item_view_message in list_view_message_private:
						ob_attachment = item_view_message.have_attachment()
						if ob_attachment :
								url_atta = ob_attachment.get_url()
						else:
								url_atta = None

						content = item_view_message.message.content
						excerpt = strip_tags(content)[:61].rstrip() + '...'

						vector_view_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject), ('mensaje',content), ('excerpt', excerpt), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M")),('adjunto',url_atta)]))

					retorno = vector_view_message_private

				else:
					vector_view_message_no_private = []
					list_view_message_no_private = View_Messages_User.objects.filter(user=ob_user ,private = False).order_by('-date_added')[lim_inf:lim_sup]

					for item_view_message in list_view_message_no_private:
						ob_attachment = item_view_message.have_attachment()
						if ob_attachment :
								url_atta = ob_attachment.get_url()
						else:
								url_atta = None

						content = item_view_message.message.content
						excerpt = strip_tags(content)[:61].rstrip() + '...'

						vector_view_message_no_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',content), ('excerpt', excerpt), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M")),('adjunto',url_atta)]))

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
			retorno = dict([('id',ob_view_message.id),('asunto',ob_view_message.message.subject),('mensaje',ob_view_message.message.content), ('esvisto',ob_view_message.seen), ('fecha',ob_view_message.message.date_added.strftime("%Y-%m-%d %H:%M")),('adjunto',url_atta)])

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
						ob_viewmessage.seen_date = datetime.now()
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
			ob_viewmessage = View_Messages_User.objects.filter(user=id_user).update(seen=True, seen_date=datetime.now())
			retorno = {'error':0}
			return HttpResponse(json.dumps(retorno),content_type="application/json")


	def post(self,request,*args,**kwargs):

		#Crear Mensaje

		subject = request.POST.get('subject')
		json_recipients = request.POST.get('users')
		content_men = request.POST.get('message')
		private = False if request.POST.get('isPrivate') is None or request.POST.get('isPrivate') == 'false' else True
		admin_user = User.objects.get(id=request.user.id)

		if subject and json_recipients and content_men:

			new_mensaje = Message(sender=request.user,subject=subject,content=content_men)
			new_mensaje.save()
			recipients =json.loads(json_recipients)
			ob_users= User.objects.none()

			for receiver in recipients['users']:
				if receiver == 'todos':
					item_user =  User.objects.all()
				else :
					if  receiver == 'estudiante' or receiver == 'egresado' :
						item_user = User.objects.filter(userext__profile__name=receiver)
					elif receiver.find("semestre_") != -1:
						array=receiver.split("_")
						item_user = User.objects.filter(profilemeta__key = array[0], profilemeta__value=array[1])
					else:
						item_user = User.objects.filter(username=receiver)
				ob_users = ob_users | item_user
			for ob_user in  ob_users:
				if ob_user:
					# pass
					newView=View_Messages_User(message=new_mensaje,user=ob_user,private=private)
					newView.save()
					from_attachment = fromAttachment(request.POST, request.FILES)
					if from_attachment.is_valid():
						new_att=from_attachment.save(commit=False)
						new_att.message = new_mensaje
						new_att.save()
			if private:
				notificar_mensaje(json_recipients,subject,content_men,admin_user)

			retorno = {'error':0,'message':'/mensajes/' + str(new_mensaje.pk)}
		else:
			retorno = {'error':1,'message':'Los campos enviados no son válidos'}

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
