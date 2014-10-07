'use strict';

var gulp								= require('gulp'),
		nib									= require('nib'),
		rename							= require('gulp-rename'),
		stylus							= require('gulp-stylus'),
		staticPath					=	'./public/static/';

/*
 * Assets processing and livereload enabling
 * [css] : compile stylus files into css
 * [html]: reload page
*/

// Process CSS files and reload the web browser
gulp.task('css', function() {
	gulp.src( staticPath + 'css/main.styl' )
		.pipe(stylus({
			use: nib(),
			compress: true
		}))
		.pipe(rename('main.min.css'))
		.pipe(gulp.dest( staticPath + 'css/min/'));

		// @TODO
		// Incorporar livereload para cambios CSS
});

// @TODO
// Incorporar livereload para cambios HTML
// Ver: django-livereload, gulp-livereload

// Watch file changes
gulp.task('watch', function() {
	gulp.watch([ staticPath + 'css/**/*.styl'], ['css']);
});

gulp.task('default', [ 'css', 'watch' ]);