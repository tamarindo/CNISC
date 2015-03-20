# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse 
from django.shortcuts import redirect
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.mail.message import EmailMultiAlternatives
from django.views.generic import View
from apps.userManager.forms import from_foto , from_recuperar_pass
from apps.userManager.models import UserExt , TempKeys
from apps.main.utilities import *
from random import choice
import pprint
import json
import re
from datetime import datetime
from datetime import timedelta
#  ----------------------------------------------------------   login  ---------------------------------------------------------------------------- 
def v_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def login(request):
	mensaje=False
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
					mensaje="Su Usuario no esta Activo"
			else:
				mensaje="Su username o password estan incorrentos, vuelvelo a intentar"

	formularioLogin = AuthenticationForm(request.POST)
	if mensaje:
		return render_to_response('login.html',{'mensaje':mensaje,'formulario':formularioLogin},context_instance=RequestContext(request))
	else:
		return render_to_response('login.html',{'formulario':formularioLogin},context_instance=RequestContext(request))
#  ----------------------------------------------------------   Recuperar  ---------------------------------------------------------------------------- 
def recuperar_pass(request):
	if request.method == 'POST':
		email=request.POST.get('email')
		EmailV = re.match("^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,10}$",email)
		if EmailV != None:
			ob_user = User.objects.filter(email = email)
	 		if not ob_user:
				ob_user = UserExt.objects.filter(email_alt = email)				

			if ob_user:

				longitud = 18
				valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
				p = ""
				p = p.join([choice(valores) for i in range(longitud)])				
				Keys = TempKeys(key=p,user=ob_user[0])
				Keys.save()

				email_context = {
					'key'    : p,
			        'titulo' : 'Recuperación de password',
			        'url'    : 'localhost:8000/verificar_keys', 
			        'usuario': ob_user[0].get_full_name(),
			    }

				send_email(email_context,'email_keys_send.html','Recupera Password CNISC','no-reply@isc.edu.co',[email]);
				mensaje = 'Se ha enviado un correo con las instruciones para recuperar su contraseña'
				
			else :
				mensaje = 'No existe este algún usuario con este correo'
		else :
			mensaje = 'El correo no tiene el formato correcto'
	else :
		mensaje = ''
	template = 'recuperar_pass.html'
	return render_to_response(template,{'mensaje':mensaje},context_instance=RequestContext(request))


def verificar_keys(request,args):
	if request.method == 'POST':
		pprint.pprint(args)
		ob_key = TempKeys.objects.get_or_none(key=args)
		if ob_key :
			hora_actual = datetime.now()	
			delta = timedelta(hours=-24)
			if ob_key.date_added.replace(tzinfo=None) + delta <= hora_actual :
				password1=request.POST.get('password1')
				password2=request.POST.get('password2')
				if password1 == password2:
					ob_user = User.objects.get(pk=ob_key.user.pk)
					ob_user.set_password("password1")
					ob_user.save()

					return redirect(reverse('login'))
				else :
					mensaje = " Las password no coinciden "
			else :
				mensaje = "La Key a vencido porfavor genera una nueva"
		else :
			mensaje = " key no valida"		
	
	template = 'verificar_pass.html'
	return render_to_response(template,{'key':args},context_instance=RequestContext(request))

# -------------------------------------------- API V2 ---------------------------------------------
		
class Email(View):

	http_method_names = ['pull']

	def put(self,request,*args,**kwargs):

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


def aviso_bienvenida(request):
	if request.user.is_authenticated() :
		ob_userext=UserExt.objects.get(user=request.user)
		ob_userext.welcome_message=True
		ob_userext.save()
					
		retorno = {'error':0}
	else:
		retorno = {'error':1,'msj':'Usuario no autentificado'}
	return HttpResponse(json.dumps(retorno),content_type="application/json")			

def eliminar_foto(request):
	if request.user.is_authenticated() :
		ob_UserExt=UserExt.objects.get(user=request.user)  
        if ob_UserExt:
            ob_UserExt.foto.delete(save=True) 
	return  HttpResponseRedirect(reverse_lazy("preferences"))

def change_foto(request):	
	if request.user.is_authenticated() :
		pprint.pprint(request.user)
		ob_userext=UserExt.objects.get(user=request.user)
		form = from_foto(request.POST, request.FILES,instance=ob_userext)
        if form.is_valid():
        	form.save()
	return  HttpResponseRedirect(reverse_lazy("preferences"))


def changeemail(request):
	if request.user.is_authenticated() :
		email=request.POST.get('email')
		id_user = request.user.id
		ob_user = User.objects.get(id=id_user)
		EmailV = re.match("^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,10}$",email)
		if EmailV != None:
			ob_user.userext.email_alt=email
			ob_user.userext.save()
		else:
			ob_user.userext.email_alt=""
			ob_user.userext.save()			

	return  HttpResponseRedirect(reverse_lazy("preferences"))	



	