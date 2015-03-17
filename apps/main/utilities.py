# coding=utf-8
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.mail.message import EmailMultiAlternatives

def ValidateEmail( email ):    
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def send_email(json,template,asunto,remitente,destinatario):

	email_html = render_to_string(template, json)
    # se quitan las etiquetas html para que quede en texto plano
	# email_text = strip_tags(email_html)
	correo = EmailMultiAlternatives(
        asunto,  # Asunto
        email_html,  # contenido del correo
        remitente,  # quien lo envía
        destinatario,  # a quien se envía
    )
    # se especifica que el contenido es html
	correo.attach_alternative(email_html, 'text/html')
    # se envía el correo
	correo.send()