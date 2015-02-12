from django import forms
from apps.userManager.models import UserExt

class from_foto(forms.ModelForm):
   
    
    class Meta:
    	model = UserExt 
    	fields = ['foto']