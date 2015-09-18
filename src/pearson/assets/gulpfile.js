var gulp = require('gulp');

// Libraries
var addsrc = require('gulp-add-src');
var concat = require('gulp-concat');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var sass   = require('gulp-sass');
var uglify = require('gulp-uglify');


// Variables
var options = {
  'minify': true
};

var paths = {
  'bower': 'bower_components',
  'dist': '../static/pearson'
};

var tasks = {
  'scripts': 'scripts',
  'styles': 'styles',
  'fonts': 'fonts',
  'default': 'default'
};


// Scripts Task
gulp.task(tasks.scripts, function () {
  var scripts = gulp.src([
      paths.bower + '/jquery/dist/jquery.js',                           // JQuery
      paths.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js',  // Bootstrap
      paths.bower + '/select2/select2.js',                              // Select2
      'scripts/application.js'
    ])
    .pipe(concat('application.min.js'));

  if (options.minify) {
    scripts.pipe(uglify());
  }

  scripts.pipe(gulp.dest(paths.dist + '/scripts'));

  // Modernizr
  var modernizr = gulp.src([
      paths.bower + '/modernizer/modernizr.js'
    ])
    .pipe(rename('modernizr.min.js'));

  if (minify) {
    modernizr.pipe(uglify());
  }

  modernizr.pipe(gulp.dest(paths.dist + '/scripts'));
});


// Styles Task
gulp.task(tasks.styles, function () {
  var styles = gulp.src(['styles/application.scss'])
    .pipe(sass({
      includePaths: [
        paths.bower + '/bootstrap-sass/assets/stylesheets',   // Bootstrap
        paths.bower + '/fontawesome/scss'                     // Font Awesome
      ]
    }))
    .pipe(addsrc(paths.bower + '/select2/select2.css'))                         // Select2
    .pipe(addsrc(paths.bower + '/select2-bootstrap-css/select2-bootstrap.css')) // Select2 Bootstrap
    .pipe(concat('application.min.css'));

  if (options.minify) {
    styles.pipe(minify({
      keepSpecialComments: 0
    }));
  }

  styles.pipe(gulp.dest(paths.dist + '/styles'));
});


// Fonts Task
gulp.task(tasks.fonts, function () {
  // Bootstrap Glyphicons
  gulp.src(
    paths.bower + '/bootstrap-sass/assets/fonts/**/*'
  )
  .pipe(gulp.dest(paths.dist + '/fonts'));

  // Font Awesome
  gulp.src(
    paths.bower + '/fontawesome/fonts/*'
  ).pipe(gulp.dest(paths.dist + '/fonts'));

  // Select 2
  gulp.src([
    paths.bower + '/select2/select2.png',
    paths.bower + '/select2/select2-spinner.gif'
  ]).pipe(gulp.dest(paths.dist + '/styles'))
});


// Default Task
gulp.task(tasks.default, [tasks.scripts, tasks.styles, tasks.fonts]);
