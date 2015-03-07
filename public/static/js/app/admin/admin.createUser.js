/*
 * Controlador para validar el formulario, interactuar y crear un 
 * nuevo usuario
*/

(function(){

	'use strict';

	var app = angular.module('createUser', ['ngCookies', 'Api', 'shareComponents'])

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


	// Controlador para validar el formulario
	// Enviar request de crear usuario
	// y renderizar la respuesta de la API en un alert
	app.controller('CreateUserController', ['$scope', 'ApiUser', 
	  function($scope, ApiUser) {

		$scope.isHidden = true;

		$scope.alert = {
			message: '',
			type: ''
		};

		// Función con la que se procesa el envío del form
		$scope.submit = function() {
			ApiUser.new(
				$.param( $scope.user)
			)
			.$promise.then(function( response ) {

				// Cree la alerta con el valor de respuesta
				$scope.alert = {
					message: response.message,
					type: ( parseInt(response.error, 10) ) ? 'error' : 'success'
				};

				// Muestre la alerta
				$scope.isHidden = false;

				// Scroll al top
				document.body.scrollTop = document.documentElement.scrollTop = 0;

			});
		}

		// Funcion que esconde el alert
		$scope.hide = function() {
			$scope.isHidden = true;
		}

	}]);

})();