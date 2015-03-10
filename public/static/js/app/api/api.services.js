/*
 * Servicios de la API
 * Brinda servicios que provee abstracción de la API
*/

(function(){
	'use strict';

	var api = angular.module('Api', ['ngResource'] );

	api.constant( 'ApiUrl', {
		messaging : '/api/mensajes/',
		oauth : '/api/oauth/',
		alerts: '/api/avisos/',
		newUser: '/usuarios/crear/'
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
					private		: 0
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

	// Factoria para actuar sobre avisos
	api.factory('ApiAlerts', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.alerts + ':slug', { slug: "@slug" }, {
			'update' : {
				method: 'POST'
			}
		});

	}]);

	// Factoria para crear un nuevo usuario
	api.factory('ApiUser', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.newUser, {}, {
			'new' : {
				method: 'POST'
			}
		});

	}]);

})();