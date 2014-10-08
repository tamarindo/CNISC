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

Aunque es opcional, se recomienda instalar la aplicación en un entorno virtual `virtualenv` de Python para que las dependencias instaladas no causen conflictos. En la instalación hacemos uso del wrapper [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

También se ha utilizado [PIP de Python](#) para manejar paquetes. Debe instalarse.


## Instalación
1. Clonar el repositorio usando git

		$ git clone https://github.com/tamarindo/CNISC.git && cd CNISC

2. Recomendación: Iniciar un nuevo entorno virtual `virtualenv`
		
		$ mkvirtualenv cniscenv

3. Sincronizar paquetes y base de datos

	Se instalarán los paquetes necesarios a través de los gestores pip, npm y bower. Además se sincronizará la base de datos. El proceso pedirá crear un nuevo super usuario para la Aplicación.

		$ make sync

4. Compilar assets

		$ gulp

5. Iniciar servidor

		$ python manage.py runserver

La aplicación será accesible desde `http://127.0.0.1:8000/`