# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.template import RequestContext  # para hacer funcionar {% csrf_token %}
from django.contrib.auth.models import User

from apps.main.models import *
from apps.main.utilities import *
from apps.oauthSocial.models import *
from apps.oauthSocial.utilis import *
from apps.parceadores.models import *
from apps.tags.models import *
from apps.messaging.forms import fromAttachment
from apps.userManager.models import *
from apps.userManager.forms import from_foto
from apps.userManager.urls import userManager_urls
from apps.messaging.models import View_Messages_User , Message
from apps.parceadores.froms import ImportXLSForm
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie

from pprint import pprint
import json
from random import choice

@ensure_csrf_cookie

# URL PUBLICAS RENDER TEMPLATE

# vistas compartidas
def home(request):
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:
			id_msj=request.GET.get('id_msj')
			if id_msj :
				ob_message = Message.objects.get_or_none(pk=id_msj)
			ob_fromAttachment = fromAttachment()
			messages_send=Message.objects.filter(sender=ob_user).order_by('-date_added')
			template="mainAdminTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))
		else :
			vector_temp_message=[]
			messages_not_seen=len(View_Messages_User.objects.filter(user=ob_user,seen=False))
			list_view_message=View_Messages_User.objects.filter(user=ob_user,private=False).order_by('-date_added')[0:5]
			for item_view_message in list_view_message:
				ob_attachment = item_view_message.have_attachment()
				if ob_attachment :
					url_atta = ob_attachment.get_url()
				else:
					url_atta = None
				vector_temp_message.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M")),('adjunto',url_atta)]))

			vector_temp_message_private=[]
			list_view_message_private=View_Messages_User.objects.filter(user=ob_user,private=True).order_by('-date_added')[0:5]

			for item_view_message in list_view_message_private:
				ob_attachment = item_view_message.have_attachment()
				if ob_attachment :
					url_atta = ob_attachment.get_url()
				else:
					url_atta = None
				vector_temp_message_private.append(dict([('id',item_view_message.id),('asunto',item_view_message.message.subject),('mensaje',item_view_message.message.content), ('esvisto',item_view_message.seen), ('fecha',item_view_message.message.date_added.strftime("%Y-%m-%d %H:%M")),('adjunto',url_atta)]))

			dic_messages= json.dumps({'mensajes':vector_temp_message,'mensajes-privados': vector_temp_message_private})

			template="mainUserTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse("login"))

def preferences(request):
	if request.user.is_authenticated():
		ob_user=User.objects.get(id=request.user.id)
		if ob_user.userext.profile.is_admin == 1:
			estado_twitter=verificar_conexion_twitter(request.user)
			template="preferencesAdminTemplate.html"
		else:
			fromfoto=from_foto()
			estado_twitter=verificar_conexion_twitter(request.user)
			estado_facebook = verificar_conexion_facebook(request.user)
			template="preferencesUserTemplate.html"
		return render_to_response(template,locals(),context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse("home"))

def panelUseradmin(request):
	ob_user=User.objects.get(id=request.user.id)
	if ob_user.userext.profile.is_admin == 1:
		list_usuarios = User.objects.filter(is_staff=0)

		v_list_users = []

		for user in list_usuarios :
			v_list_users.append( dict([
				('id', user.pk),
				('cod', user.username),
				('name', user.get_full_name()),
				('email', user.email),
				('imgUrl', '' + user.userext.profile_image_url() ),
				])
			)

		dic_list_users = json.dumps(v_list_users)

		template="userAdminTemplate.html"
		return render_to_response(template,locals(),context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse("home"))


def panelCrearUsuarios(request):
	ob_user = User.objects.get(id=request.user.id)

	if ob_user.userext.profile.is_admin :

		if 'GET' == request.method :
			template="userCreateTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))

		elif 'POST' == request.method :

			nombre = request.POST.get('nombre')
			apellidos = request.POST.get('apellidos')
			email = request.POST.get('email')
			codigo = request.POST.get('codigo')
			error = 0
			message = ''

			if  nombre != "" and apellidos != "" and email != "" and ValidateEmail(email) and codigo != "" :

				# Creacion del usuario
				new_ob_user = User(
					first_name = nombre,
					last_name = apellidos,
					email = email,
					username = codigo
				)

				new_ob_user.set_password(codigo)

				# Informacion adicional del usuario
				new_ob_userext = UserExt(
					phone =  request.POST.get('mobile'),
					mobile = request.POST.get('mobile'),
					address = request.POST.get('address'),
					city = request.POST.get('city'),
					province= request.POST.get('province'),
					country= request.POST.get('country'),
				)

				# Validacion si el username o correo ya existen
				if User.objects.filter(username=codigo).exists() or User.objects.filter(email=email).exists() :
					return HttpResponse( json.dumps( {'error': 1, 'message': 'El usuario ya existe'} ), content_type="application/json" )

				# Agregar perfil
				# TODO: Parametrizar los tipos de perfiles permitidos
				input_perfil = request.POST.get('perfil')

				if input_perfil == 'estudiante' or input_perfil == 'egresado' or input_perfil == 'otro':
					ob_perfil = Profile.objects.get_or_none( name = input_perfil )
					new_ob_userext.profile = ob_perfil

				else :
					return HttpResponse( json.dumps( {'error': 1, 'message': 'Debe especificar un perfil'} ), content_type="application/json" )

				# Save user
				new_ob_user.save()

				# Save userExt
				new_ob_userext.user = new_ob_user
				new_ob_userext.save()

				# Save profileMeta
				if input_perfil == 'estudiante':
					ProfileMeta.objects.update_or_create(user=new_ob_user, key="semestre", defaults={'value': request.POST.get('semestre')})
					ProfileMeta.objects.update_or_create(user=new_ob_user, key="estado", defaults={'value': request.POST.get('estado')})

				elif input_perfil == 'egresado':
					ProfileMeta.objects.update_or_create(user=new_ob_user, key="cargo", defaults={'value': request.POST.get('cargo')})
					ProfileMeta.objects.update_or_create(user=new_ob_user, key="empresa", defaults={'value': request.POST.get('empresa')})

				return HttpResponse( json.dumps( {'error': 0, 'message': "/usuarios/" + str(new_ob_user.pk )} ), content_type="application/json" )

			else :
				return HttpResponse( json.dumps( {'error': 1, 'message': "Alguno de los campos no es correcto. Por favor verifiquelos"} ), content_type="application/json" )

		else:
			return HttpResponseRedirect( reverse("home") )

	else:
		return HttpResponseRedirect( reverse("home") )

class Usuario(View):

	http_method_names = ['get','pull','post','delete']

	def get(self,request,*args,**kwargs):
		# traer Usuario
		ob_user=User.objects.get(id=request.user.id)

		if ob_user.userext.profile.is_admin == 1:
			usuario=User.objects.get(pk=args[0])

			if ValidateEmail(usuario.userext.email_alt) :
				email_actual = usuario.userext.email_alt
			else :
				email_actual = usuario.email

			# Perfil del usuario
			profile = usuario.userext.profile.name
			profile_info = ProfileMeta.objects.filter(user=usuario)

			template="userEditTemplate.html"
			fromfoto = from_foto()
			return render_to_response(template,locals(),context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect(reverse("home"))


	def post(self,request,*args,**kwargs):
		if args[0] != None :
			usuario=User.objects.get(pk=args[0])
			ob_userext=UserExt.objects.get(user=usuario)

			if request.POST.get('is_active'):
				data = True
			else :
				data = False
			usuario.is_active=data

			# Cambio de password ?
			password = request.POST.get('pass')
			if password and password != "":
				usuario.set_password(password)

			usuario.save()

			if request.POST.get('email') != usuario.email :

				ob_userext.email_alt = request.POST.get('email')

			ob_userext.mobile= request.POST.get('mobile')
			ob_userext.address= request.POST.get('address')
			ob_userext.city= request.POST.get('city')
			ob_userext.province= request.POST.get('province')
			ob_userext.country= request.POST.get('country')
			ob_userext.save()

			# Actualización del Perfil
			if ob_userext.profile.name == 'estudiante' :
				ProfileMeta.objects.update_or_create(user=usuario, key='semestre', defaults={'value': request.POST.get('semestre')})
				ProfileMeta.objects.update_or_create(user=usuario, key='estado', defaults={'value': request.POST.get('estado')})
			elif ob_userext.profile.name == 'egresado' :
				ProfileMeta.objects.update_or_create(user=usuario, key='cargo', defaults={'value': request.POST.get('cargo')})
				ProfileMeta.objects.update_or_create(user=usuario, key='empresa', defaults={'value': request.POST.get('empresa')})

			# Perfil del usuario
			profile = usuario.userext.profile.name
			profile_info = ProfileMeta.objects.filter(user=usuario)

			if ValidateEmail(usuario.userext.email_alt) :
				email_actual = usuario.userext.email_alt
			else :
				email_actual = usuario.email

			fromfoto = from_foto()
			mensaje = "Usuario actualizado"
			template="userEditTemplate.html"
			return render_to_response(template,locals(),context_instance=RequestContext(request))
		else :
			return HttpResponseRedirect(reverse("home"))


	def delete(self,request,*args,**kwargs):
		pass
		# Eliminar Usaurio

def mensajeEnviado (request,*args):

	if request.user.userext.profile.is_admin == 1 :
		print args
		if args != () :
			#Enviar un solo Mensaje
			mensaje_id = int( args[0] )
			ob_message = Message.objects.get( pk = mensaje_id )
			ob_attachment = Attachment.objects.get_or_none(message =ob_message )
			template = 'adminSigleMessageTemplate.html'
			return render_to_response(template,locals(),context_instance=RequestContext(request))
	return HttpResponseRedirect(reverse("home"))# API


def changeTypeVisualization(request):
	type_visua=request.POST.get('typeVisua')
	ob_confuser=ConfUser.objects.get_or_none(user=request.user)
	if type_visua:
		ob_confuser.type_visualization = type_visua
		try:
			ob_confuser.save()
			retorno = {'error':0,'msj':''}
		except:
			retorno = {'error':1,'msj':'error al guardar'}
	else:
		retorno = {'error':1,'msj':'Faltan Parametros'}
	return HttpResponse(json.dumps(retorno),content_type="application/json")
