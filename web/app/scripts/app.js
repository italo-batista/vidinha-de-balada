'use strict';

/**
 * @ngdoc overview
 * @name baladaApp
 * @description
 * # baladaApp
 *
 * Main module of the application.
 */
angular
  .module('baladaApp', ['ui.router', 'ngAnimate'])
  .constant('RESTAPI', 'http://127.0.0.1:5000/')
  .config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        controllerAs: 'ctrl'
      })
      .state('perfil', {
        url: '/perfil/:id',
        templateUrl: 'views/perfil.html',
        controller: 'PerfilCtrl',
        controllerAs: 'ctrl'
      })
      .state('sobre', {
        url: '/sobre',
        templateUrl: 'views/sobre.html'
      })
      .state('contato', {
        url: '/contato',
        templateUrl: 'views/contato.html'
      });
    $urlRouterProvider.otherwise('/');
  });
