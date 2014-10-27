from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from apps.messaging.models import *
from apps.userManager.models import Profile
from apps.oauthSocial.models import *
from apps.tags.models import *
from apps.parceadores.models import*

import pprint

# Create your models here.
class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).order_by('-date_modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None



class ConfUser(models.Model):
	"""Extended to Django User model"""
	user = models.OneToOneField(User, verbose_name=_("Usuario"))
	email_alt = models.CharField(max_length=25, verbose_name=_("Email segundario"), null=True, blank=True)
	type_visualization = models.IntegerField(verbose_name=_("Tipo de visualizacion"), null=True, blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.user.username
		

