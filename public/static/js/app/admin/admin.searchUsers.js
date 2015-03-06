/*
 * Módulo sobre la búsqueda de usuarios para el admin
 * @url /usuarios
*/

(function(){

	'use strict';

	var app = angular.module('searchUsers', ['ngCookies', 'Api'])

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


	// Controlador que recoge los usuarios de una variable enviada 
	// renderizada por Django para iterar sobre ella y listar los usuarios
	app.controller('SearchController', ['$scope', function($scope){

		$scope.users = window.sresu;

	}]);

})();