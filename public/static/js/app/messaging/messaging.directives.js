(function(){
	'use strict';

	var messageDirectives = angular.module('messageDirectives', []);

	messageDirectives.directive('messageItem', function(){

		return {
			restrict: 'AE',
			templateUrl: '/static/js/app/messaging/partials/message-item.html'
		};

	});

})();