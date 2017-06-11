(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('HomeCtrl', function($http, RESTAPI) {
      var vm = this;
      vm.total = 0;
      vm.salariosMinimos = 0;

      vm.deputados = [
        {
          id: 3151,
          nome: "Nome do camarada",
          partido: "PR/PB",
          imagem: "http://www.camara.gov.br/internet/deputado/bandep/178957.jpg"
        },
        {
          id: 3152,
          nome: "Nome do camarada B",
          partido: "PR/PE",
          imagem: "http://www.camara.gov.br/internet/deputado/bandep/178957.jpg"
        }
      ];

      function init() {
        $http.get(RESTAPI+"gasto_anual?ano=2017").then(function(res) {
          vm.total = res.data[0];
          vm.salariosMinimos = Math.round( vm.total / 937000);
        });
      }
      init();
    });
})();
