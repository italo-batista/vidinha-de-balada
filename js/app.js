(function() {
  'use strict';

  angular
    .module('baladaApp', ['ui.router'])
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
          templateUrl: 'views/perfil.html'
        });
      $urlRouterProvider.otherwise('/');
    });
})();
