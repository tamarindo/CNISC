(function(){

	'use strict';

	/**
	 * Este script se utiliza para emular una carga de un input multipart (subida
	 * de archivos) desde un botón.
	 *
	 * El markup necesario es:

	  	<form id="update-image" action="{%url 'change_foto'%} " enctype="multipart/form-data" method="POST" >
			{% csrf_token %}
			<button class="flat button blue">Cambiar foto...</button>
			<div class="visuallyhidden">
				{{fromfoto.foto}}
				<input type="submit" class="submit" value="Submit" />
			</div>
		</form>

	 *
	*/

	var
		changeImgButton = document.querySelector('#update-image .button'),
		changeImgFile = document.querySelector('#id_foto'),
		changeImgSubmit = document.querySelector('#update-image .submit');

	// Escucha por un click en el botón, detiene su acción y llama
	// al input multipart haciendo click en él
	changeImgButton.addEventListener('click', function(e){
		e.preventDefault();
		e.stopPropagation();
		
		changeImgFile.click();
	});

	// Cuando haya cambio en el input multipart, envíe el formulario
	changeImgFile.addEventListener('change', function(e) {
		changeImgSubmit.click();
	});

})();