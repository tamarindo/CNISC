(function($){

	'use strict';

	// Script para hacer el body de igual altura que el
	// tamaño de la ventana, para así centrar todo el
	// contenido verticalmente en la página de login de inicio
	var parent = $('.login-page');

	// Make the heigth header same as viewport
	parent.css({
		'height': $(window).height() + 'px'
	});

	// And make it persistive
	$(window).resize(function() {
		parent.css({
			'height': $(window).height() + 'px'
		});
	});

}(jQuery));