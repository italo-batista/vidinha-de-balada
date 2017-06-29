(function() {
  'use strict';

  angular
    .module('baladaApp')
    .directive('cardDeputado', function() {
      return {
        templateUrl: 'web/views/card.html',
        restrict: 'E',
        scope: {
          deputado: '='
        }
      }
    });
})();
