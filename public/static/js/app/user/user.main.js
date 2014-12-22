/*
 * Archivo principal de la aplicación para el usuario
 *
*/

(function(){
	'use strict';

	var app = angular.module('user', ['shareComponents', 'Messaging', , 'ngCookies', 'Api'])

		// Cambiar el control de expresiones para prevenir 
		// inconvenientes con las de Django.
		.config(['$interpolateProvider', function($interpolateProvider){
			$interpolateProvider.startSymbol('{[{');
			$interpolateProvider.endSymbol('}]}');
		}])

		// Configurar cada solicitud AJAX para que incluya la cookie CSRF
		.run(['$http', '$cookies', function($http, $cookies) {
			$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
		}]);

	app.controller('mainController', [ '$scope', 'ApiMarkAllMessagesAsSeen' ,function($scope, ApiMarkAllMessagesAsSeen){
		
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

			// Enviar petición a la API
			ApiMarkAllMessagesAsSeen.save();

			// Ocultar menú lateral
			$scope.showMenu = false;

		};
	
	}]);

})();