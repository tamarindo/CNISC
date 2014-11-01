from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from apps.messaging.models import *
from apps.userManager.models import Profile, baseModel
#from apps.oauthSocial.models import *
#from apps.tags.models import *
#from apps.parceadores.models import*
#import pprint


class ConfUser(baseModel):

	user = models.OneToOneField(User, verbose_name=_("Usuario"))
	email_alt = models.CharField(max_length=25, verbose_name=_("Email segundario"), null=True, blank=True)
	type_visualization = models.IntegerField(verbose_name=_("Tipo de visualizacion"), null=True, blank=True)


	def __unicode__(self):
		return self.user.username
		

