(function() {
  angular.module('baladaApp')
    .directive('buscaPorNome', function ($http, RESTAPI) {
      return {
        templateUrl: 'views/directives/buscaPorNome.html',
        restrict: 'E',
        scope: {},
        link: function(scope, element, attrs) {
          scope.buscaNome = function() {
            $http.get(RESTAPI+"busca?nome="+scope.nome).then(function(res) {
              scope.resultado = res.data;
            })
          }

          scope.$watch(function() { return scope.nome; }, function(newValue, oldValue) {
                if (newValue && newValue.length > 3) {
                  scope.buscaNome();
                }
          }, true);

          scope.ativarBusca = function() {
            scope.mostrarBarraDeBusca = !scope.mostrarBarraDeBusca;
            if (!scope.mostrarBarraDeBusca) {
              scope.resultado = [];
              scope.nome = '';
            }
          }
        }
      }
  })
})();
