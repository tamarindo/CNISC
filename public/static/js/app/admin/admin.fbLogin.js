/*
 * Módulo para realizar el login en Facebook del administrador
 * Utilizando el Javascript SDK. (Graph API)
 *
 * Además de obtener el token de usuario solicita un Page Access Token con permisos
 * de escritura.
 *
 * @Reference
 * (Permissions)[https://developers.facebook.com/docs/facebook-login/permissions/v2.3]
 *
*/


(function(){

  'use strict';

  var app = angular.module('adminFBLogin', ['ngCookies', 'Api', 'FBLogin'])

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

  app.controller('FBController', ['$scope', '$fblogin', 'ApiFacebook', function($scope, $fblogin, ApiFacebook) {

    $scope.pages = [];

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
      // Al usuario autenticarse y aprobar los permisos, hay que hacer un request
      // para obtener el Page Access Token de la página que quiere enlazar.
      // Se reciben los datos y se guarda la primer página que tenga el usuario.
      // @see setFBPage()
      // @ref https://developers.facebook.com/docs/facebook-login/access-tokens#pagetokens
      //
      // @TODO permitir elegir qué página enlazar
      else if( response.status === 'authenticate.fblogin' ) {

        var account = response.data;
        var userId = FB.getUserID();
        FB.api('/'+ userId +'/accounts', function(pagesInfo) {
          console.log(pagesInfo.data);
          var firstPage = pagesInfo.data[0];
          setFBPage(firstPage, account);
        });
      }
    };

    // Guarda un page access token
    // @param (page) <object>
    //
    // @TODO validar si el usuario tienen permisos de escritura en la página
    // el atributo page.perms <array> deberá contener CREATE_CONTENT
    var setFBPage = function(page, account) {

      if( ! page ) {
        return;
      }

      ApiFacebook.save(
        $.param({
          accessToken: page['access_token'],
          userID: page['id'],
          expiresIn: account.authResponse.expiresIn
        })
      )
      .$promise.then( function(response) {
        console.log(response.message, parseInt(response.error, 10));
      });

    };

    $scope.login = function() {

      $fblogin({
        fbId: '530163547121767',
        permissions: 'email,manage_pages,publish_pages'
      })
      .then(onSucces, onError, onProgress);

    }

  }]);

})();
