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
		newUser: '/usuarios/crear/',
		tags: '/api/tags/'
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

			// método POST para crear un mensaje
			'new': {
				method: 'POST',
				headers: {
					'Content-Type': 'multipart/form-data'
				},
				transformRequest: function (data, headersGetter) {
					var formData = new FormData();
					angular.forEach(data, function (value, key) {
						formData.append(key, value);
					});

					var headers = headersGetter();
					delete headers['Content-Type'];

					return formData;
				}
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

	// Factoria para guardar los tokens de facebook
	api.factory('ApiFacebook', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.oauth + 'facebook_connect/', {}, {
			'save' : {
				method: 'POST'
			}
		});

	}]);

	// Factoria para hacer peticiones del autocompletador
	api.factory('ApiTags', ['$resource', 'ApiUrl', function($resource, ApiUrl) {

		return $resource( ApiUrl.tags + ':tag', { tag: "@tag" }, {
			'query' : {
				method: 'GET'
			}
		});

	}]);

})();