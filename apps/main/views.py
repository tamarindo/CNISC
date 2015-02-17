from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User

from apps.main.models import *
from apps.oauthSocial.models import *
from apps.oauthSocial.utilis import *
from apps.parceadores.models import *
from apps.tags.models import *
from apps.userManager.models import *
from apps.userManager.forms import from_foto
from apps.userManager.urls import userManager_urls
from apps.messaging.models import View_Messages_User
from django.views.generic import View

from django.views.decorators.csrf import ensure_csrf_cookie

import pprint
import json

@ensure_csrf_cookie

# URL PUBLICAS RENDER TEMPLATE

# vistas compartidas
def home(request):
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:
			
			vector_env_temp_message=[]
			list_view_message=Message.objects.filter(sender=ob_user)[0:5]

			for item_view_message in list_view_message:
				vector_env_temp_message.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))

			template="mainAdminTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))
		
		else :

			vector_temp_message=[]
			messages_not_seen=len(View_Messages_User.objects.filter(user=ob_user,seen=False))
			list_view_message=View_Messages_User.objects.filter(user=ob_user,private=False)[0:5]

			for item_view_message in list_view_message:
				vector_temp_message.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))

			vector_temp_message_private=[]
			list_view_message_private=View_Messages_User.objects.filter(user=ob_user,private=True)[0:5]

			for item_view_message in list_view_message_private:
				vector_temp_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))

			dic_messages= json.dumps({'mensajes':vector_temp_message,'mensajes-privados': vector_temp_message_private})		
			
			template="mainUserTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))		
	else:
		return HttpResponseRedirect(reverse("login"))

def preferences(request):
	if request.user.is_authenticated():
		fromfoto=from_foto()
		ob_user=User.objects.get(id=request.user.id)	
		if ob_user.userext.profile.is_admin == 1:		
			template="preferencesAdminTemplate.html"	
		else:
			estado_twitter=verificar_conexion_twitter(request.user)
			template="preferencesUserTemplate.html"	
		return render_to_response(template,locals(),context_instance=RequestContext(request))					
	else:
		return HttpResponseRedirect(reverse("home"))

''''
def panelUser(request):
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)	
		if ob_user.userext.profile.is_admin == 0:		
			estado_twitter=verificar_conexion_twitter(request.user)
			template="userTemplate.html"
		else:
			return HttpResponseRedirect(reverse("home"))

		return render_to_response(template,locals(),context_instance=RequestContext(request))					
	else:
		return HttpResponseRedirect(reverse("home"))'''


def panelUseradmin(request):
	ob_user=User.objects.get(id=request.user.id)
	if ob_user.userext.profile.is_admin == 1:		
		list_usuarios=User.objects.filter(is_staff=0)
		template="userAdminTemplate.html"	
		return render_to_response(template,locals(),context_instance=RequestContext(request))	
	else:
		return HttpResponseRedirect(reverse("home"))

class Usuario(View):

	http_method_names = ['get','pull','post','delete']

	def get(self,request,*args,**kwargs):
		# traer Usuario	
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:		
			usuario=User.objects.get(pk=args[0])
			pprint.pprint(usuario.userext.student.semestre)
			template="userEditTemplate.html"	
			return render_to_response(template,locals(),context_instance=RequestContext(request))	
		else:
			return HttpResponseRedirect(reverse("home"))


	def post(self,request,*args,**kwargs):
		pass
		# Crear Usuario

	def pull(self,request,*args,**kwargs):
		pass 
		# Modificar Usuario

	def delete(self,request,*args,**kwargs):
		pass
		# Eliminar Usaurio


# API


def changeTypeVisualization(request):
	type_visua=request.POST.get('typeVisua')
	ob_confuser=ConfUser.objects.get_or_none(user=request.user)
	if type_visua:
		ob_confuser.type_visualization = type_visua
		try:
			ob_confuser.save()
			retorno = {'error':0,'msj':''}
		except:
			retorno = {'error':1,'msj':'error al guardar'}	
	else:
		retorno = {'error':1,'msj':'Faltan Parametros'}
	return HttpResponse(json.dumps(retorno),content_type="application/json")


