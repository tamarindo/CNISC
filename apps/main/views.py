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
from apps.parceadores.models import *
from apps.tags.models import *
from apps.userManager.models import *

from apps.userManager.urls import userManager_urls

import pprint
import json

# URL PUBLICAS RENDER TEMPLATE
def home(request):
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:
			template="mainAdminTemplate.html"
		else :
			vector_temp_message=[]
			messages_not_seen=len(View_Messages_User.objects.filter(user=ob_user,seen=False))
			list_view_message=View_Messages_User.objects.filter(user=ob_user)[0:5]
			for item_view_message in list_view_message:
				vector_temp_message.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))]))
			vector_messages=json.dumps(vector_temp_message)
			template="mainUserTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))		
	else:
		return HttpResponseRedirect(reverse("login"))

def preferences():
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:		
			template="preferencesUserTemplate.html"	
		else:
			template="preferencesAdminTemplate.html"			
	else:
		return HttpResponseRedirect(reverse("login"))



# URL AJAX POST

def changeTypeVisualization(request):
	type_visua=request.GET.get('typeVisua')
	ob_confuser=ConfUser.objects.get_or_none(user=request.user)
	pprint.pprint(ob_confuser)
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
