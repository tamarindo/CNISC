/*
 * Archivo principal de la aplicación para el usuario
 *
*/

(function(){
	'use strict';

	var app = angular.module('user', ['shareComponents', 'messageDirectives', 'ngCookies', 'ngSanitize', 'Api'])

		// Cambiar el control de expresiones para prevenir
		// inconvenientes con las de Django.
		.config(['$interpolateProvider', function($interpolateProvider){
			$interpolateProvider.startSymbol('{[{');
			$interpolateProvider.endSymbol('}]}');
		}])

		// Configurar cada solicitud AJAX para que incluya la cookie CSRF
		.run(['$http', '$cookies', function($http, $cookies) {
			$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			$http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
			$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
		}]);

	app.controller('mainController', [ '$scope', '$timeout', 'ApiMessages' ,function($scope, $timeout, ApiMessages){

		$scope.unreadMessages = window.UNREAD_MESSAGES;
		$scope.list = [
			vector_messages['mensajes-privados'],
			vector_messages['mensajes']
		];

		$scope.is_vector_messages_empty = function() {
			if(vector_messages['mensajes-privados'].length > 0 || vector_messages['mensajes'].length > 0) {
				return false;
			}

			return true;
		}

		// Si no hay mensajes, no continue.
		if( $scope.is_vector_messages_empty() ) {
			return;
		}

		// Mostrar el mensaje seleccionado
		// Se detecta el ultimo mensaje activo por su atributo isActive
		// Si el mensaje seleccionado es el mismo activo, no se sucede nada
		// De otro caso se selecciona el nuevo mensaje y se marca como activo.
		$scope.show = function(ob) {
			var message = ob.mensaje;
			var lastActive;

			// Buscar en las dos listas
			lastActive = _.find($scope.list[0], 'isActive', true);
			if( lastActive == undefined )
				lastActive = _.find($scope.list[1], 'isActive', true);

			if(message === lastActive)
				return;

			if(lastActive != undefined)
				lastActive.isActive = false;

			message.isActive = true;
			$scope.activeMessage = message;

			markAsRead( message );
		};

		// Marca un mensaje como leído
		var markAsRead = function( message ) {

			if( message.esvisto ) {
				return ;
			}

			message.esvisto = true;
			ApiMessages.read( { id: message.id } );

			// Actualización de mensajes sin leer
			$scope.unreadMessages -= 1;
		};

		$scope.markAll = function( index ) {
			var i = 0;

			for(i; i < $scope.list[0].length; i++) {
				$scope.list[0][i].esvisto = true;
			}

			for(i = 0; i < $scope.list[1].length; i++) {
				$scope.list[1][i].esvisto = true;
			}

			// Enviar petición de marcar todo como leído a la API
			ApiMessages.read();

			// Ocultar menú lateral
			$scope.showMenu = false;

			// Resetear contador de mensajes no leídos
			$scope.unreadMessages = 0;

		};

		// Petición para cargar mensajes antiguos
		// Envía la petición de mensajes anteriores de acuerdo
		// a la longitud del vector de mensajes de $scope.list
		// @FIX sólo carga mensajes no privados
		$scope.loadMessages = function() {
			var offset = $scope.list[1].length;

			ApiMessages.query({
				offset: offset
			})
			.$promise.then( function(query) {

				// Angular guarda dos objetos al final de cada consulta.
				// Se restan para extraer los datos que se necesitan.
				var tail = query.length - 1;
				var messageList = query.slice(0, tail);

				// Agregar nuevos mensajes
				if ( messageList.length > 0 ) {
					for( var i in messageList ) {
						$scope.list[1].push( messageList[i] );
					}
				}
				// Si no hay mas mensajes, elimine el botón "Mensajes Anteriores"
				else {
					var button = document.querySelector(".messages .load-more");

					button.parentElement.removeChild( button );
					console.log("No hay más mensajes");
				}

			});
		};

		// Muestra/esconde un pequeño resumen de cada mensaje del sidebar
		// @param bool
		$scope.toggleMessageExcerpt = function( show ) {
			$scope.showMessageExcerpt = show;

			// Grabar esta preferencia en la BD
			// Nos gusta jugar con estas opciones, así que envie la solicitud
			// luego de transcurridos 3.5 segundos.
			// Son 3.5s porque YOLO

			// Si hay algun request efectúandose, cancélese y
			// genere uno nuevo.
			if( $timeout.cancel($scope.toggleMessageExcerptRequest) ) {
				// @TODO enviar solicitud API
				console.log('Cancelando solicitud');
			}
			console.log('Enviando solicitud');
			$scope.toggleMessageExcerptRequest = $timeout(function(){
				// @TODO enviar solicitud API
				console.log('Solicitud enviada: ' + $scope.showMessageExcerpt);
			}, 3500);
		};

	}]);

})();
