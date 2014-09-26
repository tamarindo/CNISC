
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from apps.main.models import *
from django.contrib.auth.models import User
import pprint
# Create your views here.
def home(request):
	if request.user.is_authenticated():
		ob_user = User.objects.get(username='admin')
		if ob_user:
			msj = " el usuario admin si existe"
		else:
			msj = " el usuario admin no existe"
		pprint.pprint(ob_user)
		template = "home.html"
		return render_to_response(template, locals(),context_instance=RequestContext(request)) 
	else:
		return HttpResponseRedirect(reverse("login"))

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