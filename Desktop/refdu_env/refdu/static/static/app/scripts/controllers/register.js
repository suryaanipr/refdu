'use strict';

/**
 * @ngdoc function
 * @name sampleAppApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sampleAppApp
 */
angular.module('sampleAppApp')
  .controller('registerCtrl',function ($scope, $http, $auth, $rootScope, $location) {
    console.log('registerCtrl');
    $scope.registration_status = " ";

   $scope.logout = function(){
        $auth.logout();
   }
   console.log($auth.getToken())
   $scope.services = [
        {ServiceID: 'cu', ServiceName: 'Customer'},
        {ServiceID: 'co', ServiceName: 'Company'},
   ];

   $scope.doRegister = function(){
        $scope.registration_status = "  ";
        $scope.registration_error = "";
        console.log($scope.ServiceID)
        if($scope.formData.password && $scope.formData.email && $scope.ServiceID){
             $auth.signup({
                    email: $scope.formData.email,
                    password: $scope.formData.password,
                    account_type: $scope.ServiceID,
                    password_change: false
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
.controller('activationCtrl',function ($scope, $http, $routeParams) {
    if(typeof $routeParams.token !== 'undefined'){
        $http({
            method: 'POST',
            url: '/auth/activate',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            data: {
                'token' : $routeParams.token
            },
        })
        .success(function (out) {
            console.log(out)
            $scope.activation_status = 'successfully activated';
        })
        .error(function(out){
            console.log(out)
            $scope.activation_status = out.error;
        })
    }
})
.directive('backImg', function(){
    return function(scope, element, attrs){
        var url = attrs.backImg;
        element.css({
            'background-image': 'url(' + url +')',
            'background-size' : 'cover',
            //'height':'100p[x'

        });
    };
});
angular.module('UserValidation', []).directive('validPasswordC', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {

              ctrl.$setValidity('noMatch', true);

                attrs.$observe('validPasswordC', function (newVal) {
                    if (newVal === 'true') {
                        ctrl.$setValidity('noMatch', true);
                    } else {
                        ctrl.$setValidity('noMatch', false);
                    }
                });
        }
    }
})

