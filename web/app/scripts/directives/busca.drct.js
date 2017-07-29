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
            $http.get(RESTAPI+"busca?nome="+scope.nome).then(function(res) {
              console.log(res);
              scope.resultado = res.data;
            })
          }
          scope.buscaNome();
        }
      }
  })
})();
