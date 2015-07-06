'use strict';

/**
 * @ngdoc function
 * @name sampleAppApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sampleAppApp
 */
angular.module('sampleAppApp')

  .controller('LoginCtrl', function ($scope, $http, $location, $rootScope) {

    $scope.doLogin = function(){
        $scope.login_status = "  ";
        $scope.login_error = "";
        if($scope.formData.password && $scope.formData.email){
          $http({
            method: 'POST',
            url: '/auth/login',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'email' : $scope.formData.email,
                'password': $scope.formData.password,
            },
        })
        .success(function (out) {

           if(out.status == 200){
                $scope.login_status = true;
                console.log(out.person[0].fields.role)
                $rootScope.role = out.person[0].fields.role;

                if($rootScope.role == 'cu'){
                    console.log('dddddddddd')
                    $location.path('/customer')
                }else if($rootScope.role = 'co'){
                    $location.path('/company')

                }else{
                    console.log('do nothing')
                }
           }else{
                $scope.login_status = false;
                $scope.login_error = out.error;
           }
        })
        .error(function (data, status) {

        });
        }else{
            console.log('value missing')
        }
    }
});


