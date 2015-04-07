from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from apps.parceadores.parcer import verificarIntegridad , CargarMatriz
from apps.parceadores.froms import ImportXLSForm
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User
import os
import xlrd
import json
import pprint
# Create your views here.




def panelCargaMasiva(request):
	if request.method == 'POST' :
	   	form = ImportXLSForm(request.POST, request.FILES)
		if form.is_valid():
			import_file = request.FILES['import_file']
			from xlrd import open_workbook
			wb = open_workbook(file_contents=import_file.read())
			hoja = wb.sheets()[0]
			matriz = []
			ban = 0
			for row in range(hoja.nrows):
				if ban :
					fila = []
					for col in range(hoja.ncols):
						fila.append(hoja.cell(row, col).value)
					matriz.append(fila)
				ban = 1
			json_error = verificarIntegridad(matriz)
			if json_error["error"] == False :
				logs  = CargarMatriz(matriz) 
				retorno = {'json_error':json_error,'logs':logs}
			else :
				retorno = {'json_error':json_error,'logs':''}		
			template="cargaMasivaTemplate.html"	
			pprint.pprint(retorno)
			xls_form = ImportXLSForm()
			return render_to_response(template,locals(),context_instance=RequestContext(request))	

	else:
		if request.user.id :
			ob_user=User.objects.get(id=request.user.id)
			if ob_user.userext.profile.is_admin == 1 :		
				template="cargaMasivaTemplate.html"	
				xls_form = ImportXLSForm()
				return render_to_response(template,locals(),context_instance=RequestContext(request))	
			else:
				return HttpResponseRedirect(reverse("home"))
		else:
			return HttpResponseRedirect(reverse("home"))
	