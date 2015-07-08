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
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            data: {
                'token' : $auth.getToken()
            },
        })
        .success(function (out) {
            console.log(out)
            $rootScope.email = out.email;
            $rootScope.role = out.role;
        })
    }

   $scope.logout = function(){
        $rootScope = null;
        $http({
            method: 'POST',
            url: '/auth/logout',
            headers: {
                'authorization': $auth.getToken(),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            data:{
                'token': $auth.getToken()
            }

        })
        .success(function (out) {
            console.log(out)
        })

        $auth.logout();
   }
});


