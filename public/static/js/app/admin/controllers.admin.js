/*
 * Controlador para validar el formulario, interactuar y crear un 
 * nuevo usuario
*/

(function(){

	'use strict';

	var app = angular.module('admin-controllers', []);

	app.controller('SearchController', ['$scope', function($scope){

		$scope.users = window.sresu;

	}]);

	app.controller('CreateUserController', ['$scope', function($scope){

	}]);

})();