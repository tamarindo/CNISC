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

		// Mostrar el mensaje seleccionado
		// Se detecta el ultimo mensaje activo por su atributo isActive
		// Si el mensaje seleccionado es el mismo activo, no se sucede nada
		// De otro caso se selecciona el nuevo mensaje y se marca como activo.
		$scope.show = function(ob) {
			var message = ob.mensaje;
			var lastActive;

			// Buscar en las dos listas
			lastActive = _.find($scope.list[0], 'isActive', true);
			if( lastActive == undefined )
				lastActive = _.find($scope.list[1], 'isActive', true);

			if(message === lastActive)
				return;

			if(lastActive != undefined)
				lastActive.isActive = false;

			message.isActive = true;
			$scope.activeMessage = message;

			markAsRead( message );
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