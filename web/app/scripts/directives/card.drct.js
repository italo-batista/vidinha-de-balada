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
        },
        link: function (scope, element, attrs) {
          scope.IsVisible = true;
          scope.hide = function ($scope) {
              scope.IsVisible = scope.IsVisible ? false : true;

          }
        }
      }
    });
})();
