/*
 * Archivo principal de la aplicación para el usuario
 *
*/

(function(){
	'use strict';

	var app = angular.module('user', ['shareComponents', 'Messaging'])

		// Cambiar el control de expresiones para prevenir 
		// inconvenientes con las de Django.
		.config(['$interpolateProvider', function($interpolateProvider){
			$interpolateProvider.startSymbol('{[{');
			$interpolateProvider.endSymbol('}]}');
		}]);

})();