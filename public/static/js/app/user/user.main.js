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

})();