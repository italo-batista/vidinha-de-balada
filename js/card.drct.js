(function() {
  'use strict';

  angular
    .module('baladaApp')
    .directive('cardDeputado', function() {
      return {
        templateUrl: 'views/card.html',
        restrict: 'E'
      }
    });
})();
