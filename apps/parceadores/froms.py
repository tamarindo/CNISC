#encoding:utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *

IMPORT_FILE_TYPES = ['.xls', ]


class ImportXLSForm(forms.Form):
    import_file = forms.FileField(
					required= True,
					label= _(u"Selecione el archivo Excel (.xls) con su información")
				)

    def clean_import_file(self):
    	import os
        import_file = self.cleaned_data['import_file']
        extension = os.path.splitext( import_file.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s no es un archivo Excel.' % extension )
        else:
            return import_file