/*
 * Controlador para validar el formulario, interactuar y crear un 
 * nuevo usuario
*/

(function(){

	'use strict';

	var app = angular.module('admin-controllers', ['Api']);

	app.controller('SearchController', ['$scope', function($scope){

		$scope.users = window.sresu;

	}]);

	app.controller('CreateUserController', ['$scope', 'ApiUser', 
		function($scope, ApiUser){

		// Función con la que se procesa el envío del form
		$scope.submit = function() {
			ApiUser.new(
				$.param( $scope.user)
			)
			.$promise.then(function( response ) {

				console.log(response);

			});

		}

	}]);

})();