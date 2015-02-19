/*
 * Componentes UI compartidos a través de todo el sitio
 *
*/

(function(){
	'use strict';

	var shareComponents = angular.module('shareComponents', ['ngAnimate']);

	// Componente UI: Alertas. Ofrece un controlador
	// para mostrar alertas y cerrarlas al dar click en su 
	// icono de cerrar 
	shareComponents.directive('cnAlert', function(){

		return {
			restrict : 'A',
			transclude : true,
			template : '<div class="suggestion" ng-transclude></div><button ng-click="hide=true" class="flat close icon-close"></button>',
		};

	});

})();