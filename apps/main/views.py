
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
import json
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

def getMessage(request):
	ob_user=User.objects.get(id=request.user.id)
	vector_view_message=[]
	list_view_message=View_Messages_User.objects.filter(user=ob_user).order_by('date_added')
	for item_view_message in list_view_message:
		vector_view_message.append(
		dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))])
		)
		pass
	pprint.pprint(vector_view_message)
	
	retorno=json.dumps(vector_view_message)
	return HttpResponse(retorno,content_type="application/json") 

def seenMessage(request):
	id_viewmessage=request.GET.get('id')
	ob_viewmessage=View_Messages_User.objects.get_or_none(id=id_viewmessage)
	exito=True
	if ob_viewmessage.seen != True:
		ob_viewmessage.seen=True
		try:
			ob_viewmessage.save()
		except:
			exito= False	
	return HttpResponse(json.dumps({'exito':exito}),content_type="application/json")

def changeTypeVisualization(request):
	type_visua=request.GET.get('typeVisua')
	ob_confuser=ConfUser.objects.get(user=request.user)
	ob_confuser.type_visualization = type_visua
	exito=True	
	try:
		ob_confuser.save()
	except:
		exito= False
	return HttpResponse(json.dumps({'exito':exito}),content_type="application/json")
