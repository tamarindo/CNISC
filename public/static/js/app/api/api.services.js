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

	// Factoria para actuar sobre mensajes
	api.factory('ApiMessages', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.messaging + ':id', { id: "@id" }, {
			// Marca todos los mensajes como leidos
			'read': {
				method: 'PUT'
			},

			// Trae información sobre un mensaje
			'query': {
				method: 'GET',
				isArray: true,
				params: {
					offset		: 10,
					isprivate	: 0
				},
			},

			// @TODO método POST para guardar un mensaje
			'save': {
				method: 'POST',
				isArray: true,
				params: {
					asunto			: '(Sin asunto)',
					destinatarios	: '',
					cuerpo 			: '',
					adjuntos 		: ''
				},
			}

		});

	}]);

})();