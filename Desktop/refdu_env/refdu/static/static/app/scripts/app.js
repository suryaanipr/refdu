'use strict';

/**
 * @ngdoc overview
 * @name sampleAppApp
 * @description
 * # sampleAppApp
 *
 * Main module of the application.
 */
angular
  .module('sampleAppApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
  })
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/app/views/login.html',
        controller: 'LoginCtrl'
      })
      .when('/home', {
        templateUrl: 'static/app/views/main.html',
      })
      .when('/register', {
        templateUrl: 'static/app/views/register.html',
      })
      .otherwise({
        redirectTo: '/'
      });
  });
