from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


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

# Messages
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