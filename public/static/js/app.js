/*
 * Archivo principal de la aplicación angular
 * Define el módulo de la aplicación principal: 'cnisc'
 *
*/

(function(){
	'use strict';

	var cniscApp = angular.module('cnisc', [])

		// Cambiar el control de expresiones para prevenir 
		// inconvenientes con las de Django.
		.config(['$interpolateProvider', function($interpolateProvider){
			$interpolateProvider.startSymbol('{[{');
			$interpolateProvider.endSymbol('}]}');
		}]);

})();