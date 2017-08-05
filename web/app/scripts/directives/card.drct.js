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

          scope.maiorGasto = function(categoria) {
            var categorias = {
              'Divulgação de atividade parlamentar': 'divulgacao',
              'Combustíveis': 'combustivel',
              'Alimentação': 'alimento',
              'Escritório': 'escritorio',
              'Locação de veículos': 'locacao',
              'Passagens aéreas': 'passagem'
            }
            return categorias[scope.deputado.Maior_gasto_categoria] == categoria;
          }
        }
      }
    });
})();
