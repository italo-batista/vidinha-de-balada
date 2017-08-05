(function() {
  angular.module('baladaApp')
    .directive('buscaPorNome', function ($http, RESTAPI) {
      return {
        templateUrl: 'views/directives/buscaPorNome.html',
        restrict: 'E',
        scope: {},
        link: function(scope, element, attrs) {
          scope.nome = '';
          scope.buscaNome = function() {
            $http.get(RESTAPI+"buscaDeputado?nome="+scope.nome).then(function(res) {
              scope.resultado = res.data.deputadosId;
            })
          }

          scope.limparNome = function() {
            scope.nome = '';
          }

          scope.buscaNome();

          $(document).bind('click', function(event) {
            var isClickedElementChildOfPopup = element
                .find(event.target)
                .length > 0;

            if (isClickedElementChildOfPopup)
                return;

            scope.$apply(function(){
                scope.nome = '';
            });
          });
        }
      }
  })
})();
