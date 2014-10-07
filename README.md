# Centro de Notificación ISC
Sistema de notificaciones del programa de Ingeniería en Sistemas y Computación (ISC) de la Universidad Tecnológica de Pereira

Actualmente, el programa ISC emplea una lista de correos para comunicarse con los estudiantes del programa. Esta aplicación se ha creado para solucionar y optimizar la forma en que se manejan y gestionan las notificaciones a través de una plataforma web interactiva que permita mayor privacidad, seguridad, flexibilidad, confiabilidad y segmentación a la hora de comunicarse con los estudiantes y profesores.

Esta aplicación hace parte del proyecto de grado: Sistema de Gestión de Actividades del Programa ISC-UTP, presentado por:

* [Vanesa Gómez Londoño](mailto:vagolo@hotmail.com)
* [Daniel A. Bernal](mailto:dabernal@utp.edu.co)
* [Jonathan Álvarez González](mailto:jonalvarez@utp.edu.co)
* [Carlos A. Meneses (D)](mailto:cmeneses@gmail.com)


## Dependencias
Es necesario tener instalado [Git](http://git-scm.com), [Python (>=2.7)](https://www.python.org) y [Node.js (>=0.10)](http://nodejs.org) para correr la aplicación.

Se recomienda instalar la aplicación en un entorno virtual `virtualenv` de Python para que las dependencias instaladas no causen conflictos.

También se ha utilizado [PIP de Python](#) para manejar paquetes. Debe instalarse.


## Instalación
1. Clonar el repositorio usando git

		$ git clone https://github.com/tamarindo/CNISC.git && cd CNISC

2. Instalar dependencias requeridas
		
		$ pip install -r requirements.txt
		$ npm install

3. Configurar la base de datos

		$ python manage.py syncdb
		$ python manage.py makemigrations
		$ python manage.py migrate main

4. Compilar assets

		$ gulp

5. Iniciar servidor

		$ python manage.py runserver

La aplicación será accesible desde `http://127.0.0.1:8000/`