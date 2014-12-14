from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.main.models import *

from apps.userManager.models import Profile, baseModel

Provedores = (
    ('Facebook', 'Facebook'),
    ('Twitter', 'Twitter'),
)

# Messages
class App(baseModel):
	consumer_key = models.CharField(max_length=400, verbose_name=_("consumer_key"), null=True, blank=True)
	consumer_secret= models.CharField(max_length=400, verbose_name=_("consumer_secret"), null=True, blank=True)
	nombre = models.CharField(max_length=30, verbose_name=_("nombre"))
	provedor =  models.CharField(max_length=10, choices=Provedores, verbose_name=_("Provedores"))
	callback_url = models.CharField(max_length=500, verbose_name=_("callback url"))
	
	def __unicode__(self):
		return self.nombre

class CuentaSocial(baseModel):
	user = models.ForeignKey(User, verbose_name=_("usuario"))
	uid =  models.CharField(max_length=400, verbose_name=_("uid"), null=True, blank=True)
	app = models.ForeignKey(App, verbose_name=_("App"))
	select = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.user.username


class TokenSocial(baseModel):

	cuenta =  models.ForeignKey(CuentaSocial, verbose_name=_("CuentaSocial"))
	token = models.CharField(max_length=500, verbose_name=_("token"))
	token_secreto = models.CharField(max_length=500, verbose_name=_("token secreto"))
#	fecha_expiracion =  models.DateTimeField(verbose_name=_("fecha expiracion"), null=True)
	
	def __unicode__(self):
		return str(self.token)
