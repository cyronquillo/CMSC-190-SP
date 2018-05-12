'use strict'

let mainApp = angular.module("app", ['ngRoute']);

mainApp.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/main.html',
            controller: 'main-controller'
        })
        .otherwise({
            redirectTo: '/'
        });
})