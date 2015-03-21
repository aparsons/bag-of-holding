var gulp        = require('gulp');

var concat      = require('gulp-concat');
var minifyCSS   = require('gulp-minify-css');
var rename      = require('gulp-rename');
var sass        = require('gulp-sass');
var uglify      = require('gulp-uglify')

var paths = {
  'bower': 'bower_components',
  'assets': 'assets',
  'dist': 'project/boh/static/boh'
}

gulp.task('styles', function() {
  gulp.src([
    paths.assets + '/styles/application.scss'
  ])
  .pipe(sass({
    includePaths: [
      paths.bower + '/bootstrap-sass/assets/stylesheets',
      paths.bower + '/fontawesome/scss'
    ]
  }))
  .pipe(minifyCSS({
    keepSpecialComments: 0
  }))
  .pipe(concat('application.min.css'))
  .pipe(gulp.dest(paths.dist + '/css'));
});


gulp.task('scripts', function() {
  // JQuery + Bootstrap + Application
  gulp.src([
    paths.bower + '/jquery/dist/jquery.js',
    paths.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js',
    paths.assets + '/scripts/application.js'
  ])
  .pipe(concat('application.min.js'))
  .pipe(uglify())
  .pipe(gulp.dest(paths.dist + '/js'));

  // Modernizr
  gulp.src([
    paths.bower + '/modernizer/modernizr.js'
  ])
  .pipe(uglify())
  .pipe(rename('modernizr.min.js'))
  .pipe(gulp.dest(paths.dist + '/js'));
});


gulp.task('fonts', function() {
  // Bootstrap Glyphicons
  gulp.src(paths.bower + '/bootstrap-sass/assets/fonts/**/*')
  .pipe(gulp.dest(paths.dist + '/fonts'));
  // Font Awesome
  gulp.src(paths.bower + '/fontawesome/fonts/*')
  .pipe(gulp.dest(paths.dist + '/fonts/fontawesome'));
});


gulp.task('vendor', function() {
  gulp.src(paths.bower + '/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css')
  .pipe(minifyCSS({
    keepSpecialComments: 0
  }))
  .pipe(rename('datepicker.min.css'))
  .pipe(gulp.dest(paths.dist + '/css'));

  gulp.src(paths.bower + '/bootstrap-datepicker/dist/js/bootstrap-datepicker.js')
  .pipe(uglify())
  .pipe(rename('datepicker.min.js'))
  .pipe(gulp.dest(paths.dist + '/js'));
});


gulp.task('default', ['styles', 'scripts', 'fonts', 'vendor']);

gulp.task('watch', ['default'], function() {
  gulp.watch(paths.assets + '/styles/**/*.scss', ['styles']);
  gulp.watch(paths.assets + '/scripts/**/*.js', ['scripts']);
});
