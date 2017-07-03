(function() {
  'use strict';

  angular
    .module('baladaApp')
    .directive('cardDeputado', function() {
      return {
        templateUrl: 'views/directives/card.html',
        restrict: 'E',
        scope: {
          deputado: '='
        }
      }
    });
})();
