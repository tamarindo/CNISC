from django.contrib.auth.models import User
from apps.userManager.models import *

import pprint


def unicidad_codigo(matriz,posicion,cod,posicionact):
	unico= False
	j = 0
	for row in matriz :
		
		if row[posicion] == cod and j != posicionact :
			unico = True
		j = j + 1
	return unico

def verificarIntegridad(matriz):
	control = False
	json_error=dict()
	json_error["error"] = False
	msj_error = []
	i = 0

	for row in matriz:
		codigo=row[0]
		nombres=row[1]
		apellidos=row[2]
		tipo=row[10]
		email=row[5]

		# verificar el Numero de columnas
		if not control : # para que solo pregunte la primera vez
			if len(row) < 14:
				
				json_error["error"] = True
				msj_error.append({'msj':'la estructura del archivo esta incompleta','fila':'0','columna':'0'})


		if codigo == '' or nombres == '' or apellidos == '' or tipo == '' or email == '':
			json_error["error"] = True
			msj_error.append({'msj':'Falta algun campo obligatorio','fila':i,'columna':'X'})

		# verificar unicidad de codigo en la matriz

		if unicidad_codigo(matriz,0,codigo,i) : 
			json_error["error"] = True
			msj_error.append({'msj':'hay un codigo repetido en el archivo','fila':i,'columna':'A'})

		# verificar unicidad de el email en la bd
		
		if unicidad_codigo(matriz,4,email,i) : 
			json_error["error"] = True
			msj_error.append({'msj':'hay un email repetido en el archivo','fila':i,'columna':'E'})
		else :
			U = User.objects.filter(email = email)
			if len(U) > 0:
				if U[0].username != codigo  :
					json_error["error"] = True
					msj_error.append({'msj':'el email ya esta siendo usuado por otro usuario','fila':i,'columna':'F'})

		control = True
		# verificar unicidad de el email en la bd
	
		i=i+1

	json_error["data"] = msj_error
	
	return json_error

		

def CargarMatriz(matriz):
	cont_new=0
	cont_cam=0 
	for row in matriz:
		ob_user= User.objects.filter(username = int(row[0]))
		pprint.pprint(len(ob_user))
		if len(ob_user) > 0 :
			p_ob_user=ob_user[0]
			p_ob_user.username =int(row[0])
			p_ob_user.first_name = row[1]
			p_ob_user.last_name = row[2]
			p_ob_user.email = row[4]
			p_ob_user.save()
			
			p_ob_user.userext.mobile= int(row[5])
			p_ob_user.userext.address= row[6]
			p_ob_user.userext.city= row[7]
			p_ob_user.userext.province= row[8]
			p_ob_user.userext.country= row[9]

			p_ob_user.userext.save()
			ob_st = Student.objects.get_or_none( UserExt = p_ob_user.userext )
			ob_gt = Graduate.objects.get_or_none( UserExt = p_ob_user.userext )
			if ob_st :
				ob_st.semestre = row[11] 
				ob_st.save()
			elif ob_gt :
				ob_gt.program = 'ISC'
				ob_gt.job = row[13]
				ob_gt.scope = row[14]
				ob_gt.save()
			cont_cam = cont_cam + 1

		else :
			pprint.pprint('ww')
			new_ob_user = User(
					first_name = row[1],
					last_name = row[2],
					email = row[4],
					username = int(row[0])
				)
			new_ob_user.set_password(int(row[0]))
			new_ob_user.save()
			perfil = Profile.objects.get_or_none(name=row[10])
			# Informacion adicional del usuario
			new_ob_userext = UserExt(
					user  = new_ob_user,
					phone =  int(row[3]),
					mobile = int(row[5]),
					address = row[6],
					city = row[7],
					province = row[8],
					country = row[9],
					profile = perfil
				)
			new_ob_userext.save()
			if row[10] == 'estudiante':
				new_ob_student = Student(
					UserExt = new_ob_userext,
					semestre = row[11] ,
					academic_state = "",
					)
				new_ob_student.save()
			elif row[10] == 'engresado':
				new_ob_gratudat = Graduate(
					UserExt = new_ob_userext,
					program = 'ISC',
					job = row[13],
					scope = row[14],
					)
				new_ob_student.save()
			cont_new = cont_new + 1			
	json={'u_new': cont_new,'u_cam': cont_cam}

	return json