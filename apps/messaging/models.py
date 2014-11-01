from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from apps.userManager.models import Profile, baseModel


# Messages
class Message(baseModel):
	sender = models.ForeignKey(User, verbose_name=_("Remitente"))
	subject = models.CharField(max_length=120, verbose_name=_("Asunto"), null=True, blank=True)
	content = models.TextField( verbose_name=_("Mensaje"), null=True, blank=True)

	def __unicode__(self):
		return self.subject


class View_Messages_User(baseModel):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	user = models.ForeignKey(User, verbose_name=_("Usuario"))
	seen = models.BooleanField(verbose_name=_("Visto"), default=False)
	seen_date = models.DateTimeField(verbose_name=_("Fecha"), null=True, blank=True)

	def __unicode__(self):
		return self.message.subject

class Attachment(baseModel):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	data = models.FileField(upload_to='adjuntos', max_length=200)

	def __unicode__(self):
		return self.data