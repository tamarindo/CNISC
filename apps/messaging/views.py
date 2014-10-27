from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User

# Create your views here.

# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------
def getMessage(request):
	ob_user=User.objects.get(id=request.user.id)
	lim_inf=request.GET.get('lim_inf')
	lim_sup=request.GET.get('lim_sup')
	vector_view_message=[]
	list_view_message=View_Messages_User.objects.filter(user=ob_user, message__id__gte = lim_inf,message__id__lte = lim_sup ).order_by('date_added')
	for item_view_message in list_view_message:
		vector_view_message.append(
		dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M"))])
		)
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

def seenAllMessage(request):
	id_user=request.id
	ob_viewmessage=View_Messages_User.objects.filter(id_user).update(seen=True)
	exito=True
	if ob_viewmessage.seen != True:
		ob_viewmessage.seen=True
		try:
			ob_viewmessage.save()
		except:
			exito= False
	return HttpResponse(json.dumps({'exito':exito}),content_type="application/json")
# ------------------------------------------------------- funciones de mensaje ----------------------------------------------------------------------