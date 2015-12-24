var gulp = require('gulp');

// Libraries
var concat = require('gulp-concat');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var sass   = require('gulp-sass');
var uglify = require('gulp-uglify');


// Variables
var options = {
  'minify': false
};

var paths = {
  'bower': 'bower_components',
  'dist': '../static/frontend'
};

var tasks = {
  'scripts': 'scripts',
  'styles': 'styles',
  'fonts': 'fonts',
  'default': 'default'
};


// Scripts Task
gulp.task(tasks.scripts, function() {
  var scripts = gulp.src([
    paths.bower + '/jquery/dist/jquery.js',         // JQuery
    paths.bower + '/bootstrap/dist/js/bootstrap.js' // Bootstrap
  ]).pipe(concat('application.min.js'));

  if (options.minify) {
    scripts.pipe(uglify())
  }

  scripts.pipe(gulp.dest(paths.dist + '/scripts'))
});


// Styles Task
gulp.task(tasks.styles, function() {
  var styles = gulp.src([
    'styles/application.scss'
  ]).pipe(sass({
    includePaths: [
      paths.bower + '/bootstrap/scss',  // Bootstrap
      paths.bower + '/fontawesome/scss' // Font Awesome
    ]
  })).pipe(rename('application.min.css'));

  if (options.minify) {
    styles.pipe(minify({
      keepSpecialComments: 0
    }));
  }

  styles.pipe(gulp.dest(paths.dist + '/styles'));
});


// Fonts Task
gulp.task(tasks.fonts, function() {
  var fonts = gulp.src(
    paths.bower + '/fontawesome/fonts/*'
  ).pipe(gulp.dest(paths.dist + '/fonts'));
});


// Default Task
gulp.task(tasks.default, [tasks.scripts, tasks.styles, tasks.fonts]);
