from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from apps.parceadores.froms import ImportXLSForm

import json
import pprint
# Create your views here.


def parcear_xls(request):
    if request.method == "POST":
        form = ImportXLSForm(request.POST, request.FILES)

        if form.is_valid():
			pprint.pprint(form.__dict__)
			import_file = request.FILES['import_file']
			from xlrd import open_workbook
			wb = open_workbook(file_contents=import_file.read())
	data={'s':'ss'}
	return HttpResponse(json.dumps(data), content_type="application/json")