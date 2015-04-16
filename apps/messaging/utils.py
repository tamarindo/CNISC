from django.core.validators import validate_email


def notificarMensaje(ob_user):
	if ob_user.extuser.email_alt != None:
		email=ob_user.extuser.email_alt
	else:
		email=ob_user ValidateEmail


	return False