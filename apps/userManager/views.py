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
		pass 
		# traer Usuario

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

	def pull(self,request,*args,**kwargs):
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
	