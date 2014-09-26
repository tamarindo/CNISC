
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from apps.main.models import *
from django.contrib.auth.models import User
import pprint
# Create your views here.
def home(request):
	ob_user = User.objects.get(username='admin')
	if ob_user:
		msj = " el usuario admin si existe"
	else:
		msj = " el usuario admin no existe"
	pprint.pprint(ob_user)
	template = "home.html"

	return render_to_response(template, locals(),context_instance=RequestContext(request)) 