'use strict';

module.exports = function (grunt) {
  require('time-grunt')(grunt);
  require('load-grunt-tasks')(grunt);

  var config = {
    assets: 'appsec/assets',
    static: 'appsec/static'
  };

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    config: config,

    clean: {
      deploy: '<%= config.static %>',
      temp: '.temp'
    },

    jshint: {
      options: {
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      },
      all: [
        'Gruntfile.js',
        '<%= config.assets %>/scripts/{,*/}*.js',
        '!<%= config.assets %>/scripts/vendor/*'
      ]
    },

    sass: {
      deploy: {
        options: {
          sourceMap: true,
          includePaths: ['bower_components'],
        },
        files: [{
          expand: true,
          cwd: '<%= config.assets %>/styles',
          src: ['*.{scss,sass}'],
          dest: '.temp/styles',
          ext: '.css'
        }]
      }
    },

    uglify: {
      deploy: {
        files: {
          '<%= config.static %>/js/main.min.js': '<%= config.assets %>/scripts/*.js'
        }
      }
    },

    copy: {
      deploy: {
        files: [{
          expand: true,
          cwd: '<%= config.assets %>',
          dest: '<%= config.static %>',
          src: '*.{ico,png,txt}'
        }, {
          expand: true,
          cwd: '<%= config.assets %>/images',
          dest: '<%= config.static %>/images',
          src: '**/*'
        }, {
          expand: true,
          cwd: 'bower_components/bootstrap-sass-official/assets/fonts/bootstrap',
          dest: '<%= config.static %>/fonts/bootstrap',
          src: '*'
        }, {
          expand: true,
          cwd: 'bower_components/fontawesome/fonts',
          dest: '<%= config.static %>/fonts/fontawesome',
          src: '*'
        }, {
          expand: true,
          cwd: 'bower_components/jquery/dist',
          dest: '<%= config.static %>/js/vendor',
          src: 'jquery.min.js'
        }, {
          expand: true,
          cwd: 'bower_components/bootstrap-sass-official/assets/javascripts',
          dest: '<%= config.static %>/js/vendor',
          src: 'bootstrap.min.js'
        }]
      }
    },

    cssmin: {
      deploy: {
        options: {
          keepSpecialComments: 0
        },
        files: {
          '<%= config.static %>/css/screen.min.css': '.temp/styles/{,*/}*.css'
        }
      }
    },

    modernizr: {
      dist: {
        devFile: 'bower_components/modernizr/modernizr.js',
        outputFile: '<%= config.static %>/js/vendor/modernizr.min.js',
        files: {
          src: [
            '<%= config.static %>/js/{,*/}*.js',
            '<%= config.static %>/css/{,*/}*.css',
            '!<%= config.static %>/js/vendor/*'
          ]
        },
        uglify: true
      }
    },

    concurrent: {
      deploy: [
        'sass:deploy',
        'copy:deploy',
        'uglify:deploy'
      ]
    }

  });

  grunt.registerTask('deploy', [
    'clean',
    'concurrent:deploy',
    'cssmin:deploy',
    'modernizr',
    'clean:temp'
  ]);

  grunt.registerTask('default', [
    'jshint',
    'deploy'
  ]);

};
