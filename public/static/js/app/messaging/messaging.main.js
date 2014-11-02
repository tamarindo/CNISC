/*
 * Define controladores y directivas para
 * manipular el DOM con objetos mensajes
*/
(function(){
	'use strict';

	var messaging = angular.module('Messaging', []);

	messaging.controller('messages', ['$scope', function($scope){

		// Initiate
		var lastActiveIndex = 0;
		$scope.list = window.vector_messages;
		$scope.activeMessage = $scope.list[0];
		$scope.activeMessage.isActive = true;

		// Show the selected message
		$scope.show = function( index ) {
			if( lastActiveIndex != index ) {

				// Update the last active item
				$scope.list[lastActiveIndex].isActive = false;
				lastActiveIndex = index;

				// Update new active item
				$scope.list[index].isActive = true;
				$scope.activeMessage = $scope.list[index];
			}
		}

	}]);

})();