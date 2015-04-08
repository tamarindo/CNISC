
from django.test import TestCase

from django.contrib.auth.models import User
from .models import ProfileMeta

def createDummyUser():
	return User.objects.create_user(username='john', email='jlennon@beatles.com', password='glass onion')

class ProfileMetaMethodTest(TestCase):

	def test_actualizar_profilemeta_con_update_or_create(self):
		"""
		Si el key a crear ya existe para el usuario, el atributo value debera
		actualizarse
		"""
		user = createDummyUser()
		ProfileMeta.objects.update_or_create(user=user, key='same_key', defaults={'value' : 'A value'})
		ProfileMeta.objects.update_or_create(user=user, key='same_key', defaults={'value' : 'Some other value'})

		objects=ProfileMeta.objects.filter()

		self.assertEqual(len(objects), 1) # solo debe haber uno
		self.assertEqual(objects.first().value, 'Some other value') # el valor debe ser el del ultimo
