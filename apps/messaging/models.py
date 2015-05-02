from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from apps.userManager.models import Profile, baseModel


# Messages
class Message(baseModel):
	sender = models.ForeignKey(User, verbose_name=_("Remitente"))
	subject = models.CharField(max_length=120, verbose_name=_("Asunto"), null=True, blank=True)
	content = models.TextField( verbose_name=_("Mensaje"), null=True, blank=True)

	def __unicode__(self):
		return self.subject


class Attachment(baseModel):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	data = models.FileField(upload_to='adjuntos', max_length=200)

	def get_url(self):
		return str(settings.MEDIA_URL)+str(self.data)

	def __unicode__(self):
		return unicode(self.data) or u''




class View_Messages_User(baseModel):
	message = models.ForeignKey(Message, verbose_name=_("Mensaje"))
	user = models.ForeignKey(User, verbose_name=_("Usuario"))
	seen = models.BooleanField(verbose_name=_("Visto"), default=False)
	private = models.BooleanField(verbose_name=_("es privado"),default=False)
	seen_date = models.DateTimeField(verbose_name=_("Fecha"), null=True, blank=True)

	def __unicode__(self):
		return self.message.subject

	def have_attachment(self):
		ob_a=Attachment.objects.get_or_none(message=self.message)
		if ob_a:
			return ob_a
		else:
			return False
