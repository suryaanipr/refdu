'use strict';

/**
 * @ngdoc function
 * @name sampleAppApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sampleAppApp
 */
angular.module('sampleAppApp')

  .controller('mainCtrl', function ($scope, $http, $location, $rootScope, $auth) {

  })
.controller('indexCtrl', function ($scope, $http, $location, $rootScope, $auth) {
    $scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
    if ($auth.isAuthenticated()){
        $http({
            method: 'POST',
            url: '/auth/get_user_data',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'token' : $auth.getToken()
            },
        })
        .success(function (out) {
            console.log(out)
        })

    }

   $scope.logout = function(){
        $rootScope = null;
        $auth.logout();
   }
});


