var gulp        = require('gulp');

var addsrc      = require('gulp-add-src');
var concat      = require('gulp-concat');
var minifyCSS   = require('gulp-minify-css');
var rename      = require('gulp-rename');
var sass        = require('gulp-sass');
var uglify      = require('gulp-uglify');

var paths = {
  'bower': 'bower_components',
  'assets': 'assets',
  'dist': 'project/boh/static/boh',
  'templates': {
    'reports': 'project/boh/templates/boh/reports'
  }
};

var minify = true;

gulp.task('styles', function() {
  var styles = gulp.src([
        paths.assets + '/styles/application.scss'
    ])
    .pipe(sass({
        includePaths: [
          paths.bower + '/bootstrap-sass/assets/stylesheets',
          paths.bower + '/fontawesome/scss'
        ]
    }))
    .pipe(addsrc(paths.bower + '/bootstrap-markdown/css/bootstrap-markdown.min.css'))
    .pipe(addsrc(paths.bower + '/select2/select2.css'))
    //.pipe(addsrc(paths.bower + '/select2/select2-bootstrap.css'))
    .pipe(addsrc(paths.bower + '/select2-bootstrap-css/select2-bootstrap.css'))
    .pipe(concat('application.min.css'));

  if (minify)
    styles.pipe(minifyCSS({
        keepSpecialComments: 0
    }));

  styles.pipe(gulp.dest(paths.dist + '/css'));
});

// Styles for Reports
gulp.task('report-styles', function() {
  var styles = gulp.src([
      paths.assets + '/styles/reports.scss'
    ])
    .pipe(sass({
      includePaths: [
        paths.bower + '/bootstrap-sass/assets/stylesheets',
        paths.bower + '/fontawesome/scss'
      ]
    }))
    .pipe(rename('base.css'));

  if (minify)
    styles.pipe(minifyCSS({
      keepSpecialComments: 0
    }));

  styles.pipe(gulp.dest(paths.templates.reports));
});


gulp.task('scripts', function() {
  // JQuery + Bootstrap + Application
  var scripts = gulp.src([
    paths.bower + '/jquery/dist/jquery.js',
    paths.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js',
    paths.bower + '/markdown/lib/markdown.js',
    paths.bower + '/bootstrap-markdown/js/bootstrap-markdown.js',
    paths.bower + '/select2/select2.js',
    paths.assets + '/scripts/application.js'
  ])
  .pipe(concat('application.min.js'));

  if (minify)
    scripts.pipe(uglify());

  scripts.pipe(gulp.dest(paths.dist + '/js'));

  // Modernizr
  var modernizr = gulp.src([
      paths.bower + '/modernizer/modernizr.js'
    ])
    .pipe(rename('modernizr.min.js'));

  if (minify)
    modernizr.pipe(uglify());

  modernizr.pipe(gulp.dest(paths.dist + '/js'));
});


gulp.task('fonts', function() {
  // Bootstrap Glyphicons
  gulp.src(paths.bower + '/bootstrap-sass/assets/fonts/**/*')
  .pipe(gulp.dest(paths.dist + '/fonts'));

  // Font Awesome
  gulp.src(paths.bower + '/fontawesome/fonts/*')
  .pipe(gulp.dest(paths.dist + '/fonts/fontawesome'));

  // Select 2
  gulp.src([
    paths.bower + '/select2/select2.png',
    paths.bower + '/select2/select2-spinner.gif'
  ]).pipe(gulp.dest(paths.dist + '/css'))
});


gulp.task('vendor', function() {
  // Bootstrap Datepicker CSS
  var datepicker_css = gulp.src(paths.bower + '/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css')
    .pipe(rename('datepicker.min.css'));

  if (minify)
    datepicker_css.pipe(minifyCSS({
      keepSpecialComments: 0
    }));

  datepicker_css.pipe(gulp.dest(paths.dist + '/css'));

  // Bootstrap Datepicker JS
  var datepicker_js = gulp.src(paths.bower + '/bootstrap-datepicker/dist/js/bootstrap-datepicker.js')
    .pipe(rename('datepicker.min.js'));

  if (minify)
    datepicker_js.pipe(uglify());

  datepicker_js.pipe(gulp.dest(paths.dist + '/js'));

  // Chart.js
  var chart_js = gulp.src(paths.bower + '/Chart.js/Chart.js')
    .pipe(rename('chart.min.js'));

  if (minify)
    chart_js.pipe(uglify());

  chart_js.pipe(gulp.dest(paths.dist + '/js'));
});


gulp.task('default', ['styles', 'report-styles', 'scripts', 'fonts', 'vendor']);


gulp.task('development', function() {
  minify = false;
  gulp.start('default');
});


gulp.task('watch', ['default'], function() {
  gulp.watch(paths.assets + '/styles/**/*.scss', ['styles', 'report-styles']);
  gulp.watch(paths.assets + '/scripts/**/*.js', ['scripts']);
});


gulp.task('watch-development', ['development'], function() {
  gulp.watch(paths.assets + '/styles/**/*.scss', ['styles', 'report-styles']);
  gulp.watch(paths.assets + '/scripts/**/*.js', ['scripts']);
});
