from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.views.generic import View

import pprint
import json
import re

#  ----------------------------------------------------------   login  ---------------------------------------------------------------------------- 
def v_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def login(request):
	mensaje=False
	print request.method
	if request.method == 'POST':
		formularioLogin = AuthenticationForm(request.POST)
		if formularioLogin.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario,password=clave)
			if acceso is not None:
				if acceso.is_active:
					auth_login(request,acceso)
					return HttpResponseRedirect(reverse("home"))
				else:
					mensaje="Su Usuario No esta Activo"
			else:
				mensaje="Su username o password estan incorrentos, vuelvelo a intentar"

	formularioLogin = AuthenticationForm(request.POST)
	if mensaje:
		return render_to_response('login.html',{'mensaje':mensaje,'formulario':formularioLogin},context_instance=RequestContext(request))
	else:
		return render_to_response('login.html',{'formulario':formularioLogin},context_instance=RequestContext(request))
#  ----------------------------------------------------------   login  ---------------------------------------------------------------------------- 





# -------------------------------------------- API V2 ---------------------------------------------
class Usuario(View):

	http_method_names = ['get','pull','post','delete']


	def get(self,request,*args,**kwargs):
		# traer Usuario
		if args == () :
			#Enviar Varios Mensajes en base a los parametros
			lim_inf=request.POST.get('lim_inf')
			lim_sup=lim_inf+50

			if lim_inf:
					vector_usuarios  = []			
					list_users = User.objects.all()[lim_inf:lim_sup] 
					for ob_user in list_users:
						vector_view_message_private.append(dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email),("phone",ob_user.userext.phone),("mobile",ob_user.userext.mobile),("address",ob_user.userext.address),("city",ob_user.userext.mobile),("province",ob_user.userext.province),("country",ob_user.userext.country),('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d "))]))
					retorno = vector_view_message_private
				
			else:
				retorno = {'error':1,'msj':'Faltan parametros'}
		else:
			#Enviar un solo Mensaje
			
			ob_user=User.objects.get(id=request.user.id)
			if ob_user != None:
				retorno = dict([('username',ob_user.username),('fist_name',ob_user.fist_name),("last_name",ob_user.last_name),("email",ob_user.email),("phone",ob_user.userext.phone),("mobile",ob_user.userext.mobile),("address",ob_user.userext.address),("city",ob_user.userext.mobile),("province",ob_user.userext.province),("country",ob_user.userext.country),('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d "))])
			else:
				retorno = {'error':1,'msj':'usuario inexistente'}		
		
		return HttpResponse(json.dumps(retorno),content_type="application/json")

	def post(self,request,*args,**kwargs):
		pass
		# Crear Usuario

	def pull(self,request,*args,**kwargs):
		pass 
		# Modificar Usuario

	def delete(self,request,*args,**kwargs):
		pass
		# Eliminar Usaurio



		
class Email(View):

	http_method_names = ['pull']

	def put(self,request,*args,**kwargs):
		email=request.POST.get('email')
		if email:
			id_user = request.user.id
			ob_user = User.objects.get(id=id_user)
			EmailV = re.match("^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,10}$",email)
			if EmailV != None:
				ob_user.confuser.email_alt=email
				try :
					ob_user.confuser.save()
					retorno = {'error':0}
				except :
					retorno = {'error':1,'msj':'error al guardar'}

			else :
				retorno = {'error':1,'msj':'error en el formato'}			
		else:	
			retorno = {'error':1,'msj':'valores insuficientes'}
		return HttpResponse(json.dumps(retorno),content_type="application/json")




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


def aviso_bienvenida():
	if request.user.is_authenticated() :
		ob_userext=UserExt.objects.get(user=request.user)
		ob_userext.welcome_message=True
		ob_userext.save()
					
		retorno = {'error':0}
	else:
		retorno = {'error':1,'msj':'Usuario no autentificado'}
	return HttpResponse(json.dumps(retorno),content_type="application/json")			


# -------------------------------------------- API V1 ---------------------------------------------
def changeemail(request):
	email=request.POST.get('email')
	if email:
		id_user = request.user.id
		ob_user = User.objects.get(id=id_user)
		EmailV = re.match("^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,10}$",email)
		if EmailV != None:
			ob_user.confuser.email_alt=email
			try :
				ob_user.confuser.save()
				retorno = {'error':0}
			except :
				retorno = {'error':1,'msj':'error al guardar'}

		else :
			retorno = {'error':1,'msj':'error en el formato'}			
	else:	
		retorno = {'error':1,'msj':'valores insuficientes'}
	return HttpResponse(json.dumps(retorno),content_type="application/json")			
	