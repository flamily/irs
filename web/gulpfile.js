var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var plumber = require('gulp-plumber');
var notify = require('gulp-notify');
var runSequence = require('run-sequence').use(gulp);
var csso = require('gulp-csso');

gulp.task('default', function (callback) {
  runSequence(['sass', 'js', 'watch'],
    callback
  )
});

gulp.task('watch', function(){
  gulp.watch('static/scss/**/*.scss', ['sass']);
  gulp.watch('static/js/**/*.js', ['js']);
  // Other watchers
});

gulp.task('sass', function() {
  return gulp.src('static/scss/**/*.scss')   
    .pipe(plumber({errorHandler: notify.onError("Error: <%= error.message %>")}))
    .pipe(sass())
    .pipe(concat('style.css'))
    .pipe(csso())
    .pipe(gulp.dest('static/dist/'))
});

gulp.task('js', function() {
  return gulp.src('static/js/**/*.js')
    .pipe(plumber({errorHandler: notify.onError("Error: <%= error.message %>")}))
    .pipe(concat('dist.js'))
    .pipe(gulp.dest('static/dist/'))
});
