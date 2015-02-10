/*
 * Define controladores y directivas para
 * manipular el DOM con objetos mensajes
*/
(function(){
	'use strict';

	var messaging = angular.module('Messaging', ['messageDirectives']);

	messaging.controller('messages', ['$scope', 'ApiMessages', function($scope, ApiMessages){

		// Initiate
		var lastActiveIndex = [0, 0]; // last active index, last active list

		$scope.activeMessage = $scope.list[0][0]; // First message of mensajes array

		if( !$scope.activeMessage )
			return;

		$scope.activeMessage.isActive = true;

		// Show the selected message
		$scope.show = function( index, list ) {
			var lastIndex = lastActiveIndex[0];
			var lastList = lastActiveIndex[1];
			
			if( lastIndex != index || lastList != list ) {

				// Update the last active item
				$scope.list[lastList][lastIndex].isActive = false;
				lastActiveIndex = [index, list];

				// Update new active item
				$scope.list[list][index].isActive = true;
				$scope.activeMessage = $scope.list[list][index];
			}

			// Marcar el mensaje como leido
			markAsRead( this.mensaje );
		}

		var markAsRead = function( message ) {

			if( message.esvisto ) {
				return ;
			}

			message.esvisto = true;
			ApiMessages.read( { id: message.id } );
		}

	}]);

})();