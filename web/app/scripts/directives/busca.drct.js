(function() {
  angular.module('baladaApp')
    .directive('buscaPorNome', function ($http, RESTAPI) {
      return {
        templateUrl: 'views/directives/buscaPorNome.html',
        restrict: 'E',
        scope: {},
        link: function(scope, element, attrs) {
          scope.buscaNome = function() {
            $http.get(RESTAPI+"busca?"+scope.nome).then(function(res) {
              scope.resultado = res.resultado;
            })
          }

          scope.ativarBusca = function() {
            scope.mostrarBarraDeBusca = !scope.mostrarBarraDeBusca;
          }
        }
      }
  })
})();
