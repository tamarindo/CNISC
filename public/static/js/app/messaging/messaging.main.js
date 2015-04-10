/*
 * Define controladores y directivas para
 * manipular el DOM con objetos mensajes
*/
(function(){
	'use strict';

	var messaging = angular.module('Messaging', ['messageDirectives']);

	messaging.controller('messages', ['$scope', 'ApiMessages', function($scope, ApiMessages){

		if( $scope.is_vector_messages_empty() ) {
			return;
		}

		// Initiate
		var lastActiveIndex = [0, 0]; // last active index, last active list
		$scope.activeMessage = $scope.list[0][0]; // First message of mensajes array
		$scope.activeMessage.isActive = true;

		// Mostrar el mensaje seleccionado
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
		};

		// Marca un mensaje como leído
		var markAsRead = function( message ) {

			if( message.esvisto ) {
				return ;
			}

			message.esvisto = true;
			ApiMessages.read( { id: message.id } );
		};


		// Petición para cargar mensajes antiguos
		// Envía la petición de mensajes anteriores de acuerdo
		// a la longitud del vector de mensajes de $scope.list
		// @FIX sólo carga mensajes no privados
		$scope.loadMessages = function() {
			var offset = $scope.list[1].length;

			ApiMessages.query({
				offset: offset
			})
			.$promise.then( function(query) {

				// Angular guarda dos objetos al final de cada consulta.
				// Se restan para extraer los datos que se necesitan.
				var tail = query.length - 1;
				var messageList = query.slice(0, tail);
				
				// Agregar nuevos mensajes
				if ( messageList.length > 0 ) {
					for( var i in messageList ) {
						$scope.list[1].push( messageList[i] );
					}
				}
				// Si no hay mas mensajes, elimine el botón "Mensajes Anteriores"
				else {
					var button = document.querySelector(".messages .load-more");

					button.parentElement.removeChild( button );
					console.log("No hay más mensajes");
				}

			});
		}

	}]);

})();