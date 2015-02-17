from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.main.models import *

import hashlib
# Create your models here.


GENDER_CHOICES = (
    ('M', _('Masculino')),
    ('F', _('Femenino')),
    ('N', _('No definido')),
)

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
            
class baseModel(models.Model):
    # ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()
    
	class Meta:
		abstract = True

# Data Base


# --------------------------------------
# PROFILES
# --------------------------------------

class Profile(baseModel):
	name = models.CharField(max_length=20, verbose_name=_("Nombre del tipo del perfil"), null=True, blank=True)
	abbr = models.CharField(max_length=5, verbose_name=_("Abreviacion del nombre del perfil"), null=True, blank=True)
	is_admin = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class UserExt(baseModel):
	"""Extended to Django User model"""
	user = models.OneToOneField(User, verbose_name=_("Usuario"))
	profile = models.ForeignKey(Profile, verbose_name=_("Perfil"))
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Genero"), null=True, blank=True)
	phone = models.CharField(max_length=25, verbose_name=_("Telefono"), null=True, blank=True)
	mobile = models.CharField(max_length=25, verbose_name=_("Celular"), null=True, blank=True)
	address = models.CharField(max_length=60, verbose_name=_("direccion"),null=True,blank=True)
	city = models.CharField(max_length=60, verbose_name=_("ciudad"), null=True,  blank=True)
	province = models.CharField(max_length=60, verbose_name=_("estado"), null=True,  blank=True)
	country = models.CharField(max_length=60, verbose_name=_("pais"), null=True,  blank=True)
	date_born = models.DateField(null=True, verbose_name=_("Fecha de nacimiento"),  blank=True)
	welcome_message = models.BooleanField(default=False)
	foto = models.ImageField(upload_to='perfil', verbose_name='foto de perfil',blank=True)

	def __unicode__(self):
		return self.user.username
		
	def profile_image_url(self):
		if self.foto == None or self.foto == "":
			return "http://www.gravatar.com/avatar/{}?s=300".format(hashlib.md5(self.user.email).hexdigest())
		else:
			return settings.MEDIA_URL+"/"+str(self.foto) 

class Graduate(baseModel):
	UserExt = models.OneToOneField(UserExt, verbose_name=_("UserExt"))
	program = models.CharField(max_length=50, verbose_name=_("Egresado del programa de"), null=True, blank=True)
	job = models.CharField(max_length=50, verbose_name=_("Empleo"), null=True, blank=True)
	scope = models.CharField(max_length=20, verbose_name=_("Ambito laboral"), null=True, blank=True)

	def __unicode__(self):
		return self.UserExt.user.username

class Student(baseModel):
	UserExt = models.OneToOneField(UserExt, verbose_name=_("UserExt"))
	semester = models.IntegerField(verbose_name=_("Semestre"), null=True, blank=True)
	academic_state = models.CharField(max_length=50, verbose_name=_("Estado academico"), null=True, blank=True)

	def __unicode__(self):
		return self.UserExt.user.username