from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import pprint

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



# Data Base


# --------------------------------------
# PROFILES
# --------------------------------------

class Profile(models.Model):
	name = models.CharField(max_length=20, verbose_name=_("Nombre del tipo del perfil"), null=True, blank=True)
	abbr = models.CharField(max_length=5, verbose_name=_("Abreviacion del nombre del perfil"), null=True, blank=True)
	is_admin = models.BooleanField(default=False)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.name

class Graduate(models.Model):
	profile = models.OneToOneField(Profile, verbose_name=_("Perfil"))
	program = models.CharField(max_length=50, verbose_name=_("Egresado del programa de"), null=True, blank=True)
	job = models.CharField(max_length=50, verbose_name=_("Empleo"), null=True, blank=True)
	scope = models.CharField(max_length=20, verbose_name=_("Ambito laboral"), null=True, blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.profile.name

class Student(models.Model):
	profile = models.OneToOneField(Profile, verbose_name=_("Perfil"))
	semester = models.IntegerField(verbose_name=_("Semestre"), null=True, blank=True)
	academic_state = models.CharField(max_length=50, verbose_name=_("Estado academico"), null=True, blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.profile.name



class UserExt(models.Model):
	"""Extended to Django User model"""
	user = models.OneToOneField(User, verbose_name=_("Usuario"))
	profile = models.ForeignKey(Profile, verbose_name=_("Perfil"))
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Genero"), null=True, blank=True)
	phone = models.CharField(max_length=25, verbose_name=_("Telefono"), null=True, blank=True)
	mobile = models.CharField(max_length=25, verbose_name=_("Celular"), null=True, blank=True)
	address = models.CharField(max_length=60, verbose_name=_("direccion"),null=True,)
	city = models.CharField(max_length=60, verbose_name=_("ciudad"), null=True,  blank=True)
	province = models.CharField(max_length=60, verbose_name=_("estado"), null=True,  blank=True)
	country = models.CharField(max_length=60, verbose_name=_("pais"), null=True,  blank=True)
	date_born = models.DateField(null=True, verbose_name=_("Fecha de nacimiento"),  blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.user.username

	# TODO: funcion para traer imagen de facebook

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
		
# --------------------------------------
# Messages
# --------------------------------------

class Message(models.Model):
	sender = models.ForeignKey(User, verbose_name=_("Remitente"))
	subject = models.CharField(max_length=120, verbose_name=_("Asunto"), null=True, blank=True)
	content = models.TextField( verbose_name=_("Mensaje"), null=True, blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.subject


class View_Messages_User(models.Model):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	user = models.ForeignKey(User, verbose_name=_("Usuario"))
	seen = models.BooleanField(verbose_name=_("Visto"), default=False)
	seen_date = models.DateTimeField(verbose_name=_("Fecha"), null=True, blank=True)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.message.subject

class Attachment(models.Model):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	data = models.FileField(upload_to='adjuntos', max_length=200)

	# ------ datos para todas las tablas
	is_active = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	objects = GenericManager()

	def __unicode__(self):
		return self.data
