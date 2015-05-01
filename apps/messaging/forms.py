from django import forms 
from .models import Attachment
from django.forms import ModelForm, FileField, ClearableFileInput


class fromAttachment(forms.ModelForm):
    class Meta:
    	model = Attachment 
    	fields = ['data']
    	widgets = {
    		# hook angular listener
    		'data' : ClearableFileInput(attrs={'onchange': 'angular.element(this).scope().attach(this.files)'}),
    	}