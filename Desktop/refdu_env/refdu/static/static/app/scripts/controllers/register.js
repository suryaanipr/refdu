'use strict';

/**
 * @ngdoc function
 * @name sampleAppApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sampleAppApp
 */
angular.module('sampleAppApp')
  .controller('indexCtrl',function ($scope, $http, $rootScope) {
    console.log($scope.csrf_token)
  })
  .controller('registerCtrl',function ($scope, $http) {
    console.log('registerCtrl');
     $scope.services = [
        {ServiceID: 'cu', ServiceName: 'Customer'},
        {ServiceID: 'co', ServiceName: 'Company'},
    ];

    $scope.doRegister = function(){
        console.log($scope.ServiceID)
        if($scope.formData.password && $scope.formData.email && $scope.ServiceID){
          $http({
            method: 'POST',
            url: '/auth/register',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'email' : $scope.formData.email,
                'password': $scope.formData.password,
                'account_type': $scope.ServiceID
            },
        })
        .success(function (out) {
           console.log(out)
        })
        .error(function (data, status) {

        });
        }else{
            console.log('value missing')
        }
    }
})
  .constant("CSRF_TOKEN", '{{ csrf_token() }}')

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

