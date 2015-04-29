/*
 * Aplicacion que provee el controlador para autocompletar la lista de contactos
 * validar y enviar el mensaje
 * 
 * @require lodash
 */

 (function(){

   'use strict';

   var app = angular.module('createMessage', ['ngCookies', 'Api'])

		// Cambiar el control de expresiones para prevenir 
		// inconvenientes con las de Django.
		.config(['$interpolateProvider', function($interpolateProvider){
			$interpolateProvider.startSymbol('{[{');
			$interpolateProvider.endSymbol('}]}');
		}])

		// Configurar cada solicitud AJAX para que incluya la cookie CSRF
		.run(['$http', '$cookies', function($http, $cookies) {
			$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
			$http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
			$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
		}]);


	// Controlador para el formulario. Lo valida, previsualiza y envía.
	app.controller('formController', ['$scope', 'ApiTags', function($scope, ApiTags){

		$scope.message = {};
    $scope.hideSpinner = true;
    $scope.ccList = []; // Carga los usuarios recibidos por la API para autocompletar
    $scope.selectedUsers = []; // Usuarios seleccionados para enviar mensajes


    // Determina si se debe esconder la lista de autocompletado
    $scope.hideList = function() {
      return $scope.ccList.length === 0;
    }


    // Determina si se debe esconder la lista de usuarios seleccionados
    $scope.hideSelectedUsers = function() {
      return $scope.selectedUsers.length === 0;
    }


    // Valida si un usuario ya está incluido en la lista de envíos
    // @return bool
    var isUserAdded = function( user ) {
      var index = _.findIndex($scope.selectedUsers, function(u) {
        return u.username === user.username;
      });

      return (index === -1 ? false : true);

    };


    // Función de autocompletado
    // Hace peticiones a la API según una cadena y presenta las coincidencias
    // Sólo se hacen llamados cuando el texto ingresado es mayor de 4 caracteres
    $scope.autocomplete = function() {
      var key = $scope.message.to;

      if( key.length < 4 ) {
        return;
      }
      
      $scope.ccList = [];

      $scope.hideSpinner = false;

      ApiTags.query({tag: key})
      .$promise.then(function(response) {
        $scope.hideSpinner = true;

        var isError = parseInt(response.error, 10);
        if(isError) {
          console.log('Amm.. algo salió mal con el autompletador o no se encontró lo que se buscaba. ' + isError);
          return -1;
        }

        // Angular guarda dos objetos al final de cada consulta.
        // Se restan para extraer los datos que se necesitan.
        var list = response.data;

        // Agregar nuevos mensajes
        if ( list.length > 0 ) {
          for( var i in list ) {
            if( isUserAdded(list[i]) ) {  // O(n^2) :/
              list[i].selected = true;
            }
            $scope.ccList.push( list[i] );
          }
        }

      });
    }


    // Agrega un usuario a las listas
    $scope.add = function(user, e) {

      // Si el usuario seleccionado ya existe, se elimina su selección y de la lista
      if( isUserAdded(user) ) {
        user.selected = false;
        $scope.remove(user, e);
        return;
      }

      user.selected = true;
      $scope.selectedUsers.push( user );

      if(e) {
        e.stopPropagation();
        e.preventDefault();
      }
    }


    // Eliminar un usuario de las listas
    $scope.remove = function(user, e) {
      _.remove($scope.selectedUsers, function(u) {
        return u.username === user.username;
      });

      if(e) {
        e.stopPropagation();
        e.preventDefault();
      }
    }


    // Hace un reset de las listas, sucede siempre que se da click en cualquier lugar
    // Diferente al input de Destinatarios.
    $scope.reset = function() {
      $scope.ccList = [];
      $scope.message.to = '';
    }


    $scope.submit = function() {
      // @TODO 
    }


	}]);

})();