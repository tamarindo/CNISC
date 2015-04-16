/*
 * Módulo para realizar el login en Facebook
 * Utilizando el Javascript SDK.
*/


(function(){

  'use strict';

  var app = angular.module('userFBLogin', ['ngCookies', 'Api', 'FBLogin'])

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

  app.controller('FBController', ['$scope', '$fblogin', function($scope, $fblogin) {

    var onSucces = function(response) {
      console.log('success');
    };

    var onError = function(response) {
      console.log(response)
    };

    var onProgress = function(response) {

      if( response.status === 'init.fblogin' ) {
        console.log('facebook sdk initialized.'); 
      }
      else if( response.status === 'authenticate.fblogin' ) {
        // FB.getAuthResponse()
        
        // response.data.authResponse.accessToken (FB.getAccessToken())
        // response.data.authResponse.expiresIn 
        // response.data.authResponse.userID (FB.getUserId)
      }

    };

    $scope.login = function() {
      
      $fblogin({
        fbId: '530163547121767',
        permissions: 'email'
      })
      .then(onSucces, onError, onProgress);

    }

  }]);

})();