'use strict';

/**
 * @ngdoc function
 * @name sampleAppApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sampleAppApp
 */
angular.module('sampleAppApp')

  .controller('LoginCtrl', function ($scope, $location, $rootScope, $auth, $facebook) {
    $scope.forgot_password = function(){
        console.log('forgot password')
    }
    $scope.doLogin = function(){
        //$scope.login_status = "  ";
        //$scope.login_error = "";
        if($scope.formData.password && $scope.formData.email){
            $auth.login({
                    email: $scope.formData.email,
                    password: $scope.formData.password
            }).then(function(response) {
                    $auth.setToken(response.data.token);
                    $rootScope.email = response.data.email;
                    $rootScope.role = response.data.role;
                    alert($rootScope.role)
                    $location.path("/home");
                    //$auth.setToken(response.data.token);
            });
        }
    }

      $scope.isLoggedIn = false;
      $scope.login = function() {
        $facebook.login().then(function() {
          refresh();
        });
      }
      
      function refresh() {
        $facebook.api("/me").then(
          function(response) {
            $rootScope.email = response.email;
            console.log($rootScope.email);
            $location.path("/create_password")
          },
          function(err) {
            $scope.welcomeMsg = "Please log in";
          });
      }

        //refresh();

})
.controller('create_passwordCtrl', function ($scope, $location, $rootScope, $auth) {
    console.log('create_passwordCtrl')
    if(typeof $rootScope.email == 'undefined'){
        $location.path("/");
    }
    $scope.services = [
        {ServiceID: 'cu', ServiceName: 'Customer'},
        {ServiceID: 'co', ServiceName: 'Company'},
    ];
    $scope.create_password = function(){
            $scope.registration_status = "  ";
            $scope.registration_error = "";
            console.log($scope.ServiceID)
            if($scope.formData.password  && $scope.ServiceID && $rootScope.email){
                 $auth.signup({
                        email: $rootScope.email,
                        password: $scope.formData.password,
                        account_type: $scope.ServiceID,
                        password_change: true
                }).then(function(response) {
                    if(response.status == 200){
                        $auth.setToken(response.data.token);
                        $rootScope.email = response.data.email;
                        $rootScope.role = response.data.role;
                        $location.path('/home')
                    }
                });
            }
        }
})
.controller('forgotCtrl', function ($scope, $http) {
    $scope.send_forgot_link = function(){
        console.log($scope.formData.email)
        if(typeof $scope.formData.email != 'undefined'){
             $http({
                method: 'POST',
                url: '/auth/send_forgot_link',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                data: {
                    'email' : $scope.formData.email
                },
            })
            .success(function (out) {
                console.log(out)
            })
            .error(function(out){
                console.log(out)
            })
        }
    }
})
.controller('enter_passwordCtrl', function ($scope, $http, $routeParams) {
    $scope.update_forgot_password = function(){
        console.log($scope.formData.email)
        if(typeof $scope.formData.password != 'undefined' &&
           typeof $routeParams.token !== 'undefined'){

             $http({
                method: 'POST',
                url: '/auth/update_forgot_password',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                data: {
                    'token' : $routeParams.token,
                    'password': $scope.formData.password
                },
            })
            .success(function (out) {
                console.log(out)
            })
            .error(function(out){
                console.log(out)
            })
        }
    }
})





