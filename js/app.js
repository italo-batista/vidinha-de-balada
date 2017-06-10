(function() {
  'use strict';

  angular
    .module('baladaApp', ['ui.router'])
    .config(function($stateProvider, $urlRouterProvider) {
      $stateProvider
        .state('home', {
          url: '/',
          templateUrl: 'views/home.html'
        })
        .state('perfil', {
          url: '/perfil',
          templateUrl: 'views/perfil.html'
        });
      $urlRouterProvider.otherwise('/');
    });
})();
