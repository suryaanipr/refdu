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
    'ngTouch',
    'UserValidation',
    'satellizer',
    'ngFacebook'
    ])
    .config(function($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    })
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    })
    .config( function( $facebookProvider ) {
        $facebookProvider.setAppId('538108302983706');
    })
    .run( function( $rootScope ) {
          // Load the facebook SDK asynchronously
          (function(){
             // If we've already installed the SDK, we're done
             if (document.getElementById('facebook-jssdk')) {return;}

             // Get the first script element, which we'll use to find the parent node
             var firstScriptElement = document.getElementsByTagName('script')[0];

             // Create a new script element and set its id
             var facebookJS = document.createElement('script');
             facebookJS.id = 'facebook-jssdk';

             // Set the new script's source to the source of the Facebook JS SDK
             facebookJS.src = '//connect.facebook.net/en_US/all.js';

             // Insert the Facebook JS SDK into the DOM
             firstScriptElement.parentNode.insertBefore(facebookJS, firstScriptElement);
           }());
    })


    .config(function ($routeProvider, $authProvider) {

		$authProvider.logoutRedirect = '/';
		$authProvider.loginOnSignup = true;
		$authProvider.signupUrl = '/auth/register';
		$authProvider.signupRedirect = '/home';
		$authProvider.loginRedirect = '/home';



        $routeProvider
          .when('/', {
            templateUrl: 'static/app/views/login.html',
            controller: 'LoginCtrl',
            resolve: {
					authenticated: function($location, $auth) {
						if ($auth.isAuthenticated()) {
							return $location.path('/home');
						}
					}
			}
          })
          .when('/home', {
            templateUrl: 'static/app/views/main.html',
            controller: 'mainCtrl',
            resolve: {
					authenticated: function($location, $auth) {
						if (!($auth.isAuthenticated())) {
							return $location.path('/login');
						}
					}
			}

          })
          .when('/register', {
            templateUrl: 'static/app/views/register.html',
            controller: 'registerCtrl',
            resolve: {
					authenticated: function($location, $auth) {
						if ($auth.isAuthenticated()) {
							return $location.path('/home');
						}
					}
			}
          })
          .when('/create_password', {
            templateUrl: 'static/app/views/create_password.html',
            controller: 'create_passwordCtrl',
          })
          .otherwise({
            redirectTo: '/'
          });
    });
