/*
 * Archivo principal de la aplicación para el usuario
 *
*/

(function(){
	'use strict';

	var app = angular.module('user', ['shareComponents', 'Messaging', 'ngCookies', 'Api'])

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
		
		$scope.list = [];

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

		$scope.list = [
			vector_messages['mensajes-privados'],
			vector_messages['mensajes']
		];

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