from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from apps.parceadores.parcer import verificarIntegridad , CargarMatriz
from apps.parceadores.froms import ImportXLSForm
import os
import xlrd
import json
import pprint
# Create your views here.


def parcear_xls(request):
    if request.method == "POST":
        form = ImportXLSForm(request.POST, request.FILES)
        if form.is_valid():
			import_file = request.FILES['import_file']
			from xlrd import open_workbook
			wb = open_workbook(file_contents=import_file.read())
			hoja = wb.sheets()[0]
			matriz = []
			for row in range(hoja.nrows):
				fila = []
				for col in range(hoja.ncols):
					fila.append(hoja.cell(row, col).value)
				matriz.append(fila)
			json_error = verificarIntegridad(matriz)
			if json_error["error"] == False :
				logs  = CargarMatriz(matriz) 
				retorno = {'json_error':json_error,'logs':logs}
			else :
				retorno = {'json_error':json_error,'logs':''}
	return HttpResponse(json.dumps(retorno), content_type="application/json")