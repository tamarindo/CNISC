from django import forms 
from .models import App

class editApp(forms.ModelForm):
	class Meta:
		model = App
		fields = ['consumer_key','consumer_secret']