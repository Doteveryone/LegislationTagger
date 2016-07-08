module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'legitag/assets/javascript',
            src: ['*.js'], 
            dest: 'legitag/static/javascript', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'legitag/assets/vendor/foundation-sites/dist',
            src: ['**/*.js'], 
            dest: 'legitag/static/vendor/foundation-sites', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'legitag/assets/vendor/jquery/dist',
            src: ['**/*.js'], 
            dest: 'legitag/static/vendor/jquery', 
            filter: 'isFile'
          }
        ]
      }
    },
    sass: {
      options: {
        loadPath: ['legitag/assets/vendor/foundation-sites/scss']
      },
      dist: {
        files: {
          'legitag/static/css/main.css' : 'legitag/assets/sass/main.scss',
          'legitag/static/css/legislationgovuk.css' : 'legitag/assets/sass/legislationgovuk.scss'
        }
      }
    },
    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass']
      },
      scripts: {
        files: 'legitag/assets/**/*.js',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.registerTask('default',['watch']);
}