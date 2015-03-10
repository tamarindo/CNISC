from django import forms
from apps.userManager.models import UserExt

class from_foto(forms.ModelForm):
    
    class Meta:
    	model = UserExt 
    	fields = ['foto']

class from_recuperar_pass(forms.ModelForm):
    
    class Meta:
    	model = TempKeys 
    	fields = ['key']

   	