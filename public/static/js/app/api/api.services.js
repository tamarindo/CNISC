/*
 * Servicios de la API
 * Brinda servicios que provee abstracción de la API
*/

(function(){
	'use strict';

	var api = angular.module('Api', ['ngResource'] );

	api.constant( 'ApiUrl', {
		messaging : '/api/mensajes/',
		oauth : '/api/oauth/'
	});

	api.factory('ApiMarkMessageAsSeen', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.messaging + 'marcar_como_leido' );

	}])

})();