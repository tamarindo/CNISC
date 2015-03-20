from django.contrib.auth.models import User
import pprint


def unicidad_codigo(matriz,posicion,cod):
	unico=True
	for row in matriz :
		if row[posicion] == cod :
			unico = False
	return unico

def verificarIntegridad(matriz):
	


	control = False
	json_error=dict()
	json_error["error"] = False
	msj_error = []
	i = 0
	for row in matriz:
		++i 
		codigo=row[0]
		nombres=row[1]
		apellidos=row[2]
		tipo=row[10]
		email=row[5]
		
		# verificar el Numero de columnas
		if not control : # para que solo pregunte la primera vez
			if len(row) == 14:
				
				json_error["error"] = True
				msj_error.append({'msj':'la estructura del archivo esta incompleta','fila':'0','columna':'0'})


		if codigo == '' or nombres == '' or apellidos == '' or tipo == '' or email == '':
			json_error["error"] = True
			msj_error.append({'msj':'Falta algun campo obligatorio','fila':i,'columna':'X'})

		# verificar unicidad de codigo en la matriz

		if unicidad_codigo(matriz,0,codigo) : 
			json_error["error"] = True
			msj_error.append({'msj':'hay un codigo repetido en el archivo','fila':i,'columna':'A'})

		# verificar unicidad de el email en la bd
		
		if unicidad_codigo(matriz,5,email) : 
			json_error["error"] = True
			msj_error.append({'msj':'hay un email repetido en el archivo','fila':i,'columna':'5'})
		else :
			U = User.objects.filter(email = email)
			if len(U) > 0:
				if U[0].username != codigo  :
					json_error["error"] = True
					msj_error.append({'msj':'el email ya esta siendo usuado por otro usuario','fila':i,'columna':'5'})


		# verificar unicidad de el email en la bd
		control = True
	json_error["data"] = msj_error
	
	return json_error

		

	