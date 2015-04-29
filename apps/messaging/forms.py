from django import forms 
from .models import Attachment


class fromAttachment(forms.ModelForm):
    class Meta:
    	model = Attachment 
    	fields = ['data']