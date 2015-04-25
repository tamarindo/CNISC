/*
 * Aplicacion que provee el controlador para autocompletar la lista de contactos
 * validar y enviar el mensaje
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
    $scope.ccList = [];
    $scope.hideSpinner = true;

    $scope.hideList = function() {
      return $scope.ccList.length === 0;
    }

    $scope.autocomplete = function() {
      var key = $scope.message.to, m;
      if( key.length > 3 ) {

        $scope.ccList = []; // reset
        $scope.hideSpinner = false;

        ApiTags.query({tag: key})
        .$promise.then(function(response) {
          $scope.hideSpinner = true;

          var isError = parseInt(response.error, 10);
          if(isError) {
            console.log('Amm.. algo salió mal con el autompletador. ' + isError);
            return -1;
          }

          // Angular guarda dos objetos al final de cada consulta.
          // Se restan para extraer los datos que se necesitan.
          var tail = response.data.length - 1;
          var list = response.data.slice(0, tail);

          // Agregar nuevos mensajes
          if ( list.length > 0 ) {
            for( var i in list ) {
              $scope.ccList.push( list[i] );
            }
          }

        });

      }
    }

    $scope.submit = function() {
      // @TODO 
    }


	}]);

})();