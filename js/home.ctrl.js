(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('HomeCtrl', function() {
      var vm = this;
      vm.total = 61455924.06;

      vm.salariosMinimos = Math.round( vm.total / 937000);

      vm.deputados = [
        {
          id: 1,
          nome: "Nome do camarada",
          partido: "PR/PB",
          imagem: "http://www.camara.gov.br/internet/deputado/bandep/178957.jpg"
        },
        {
          id: 2,
          nome: "Nome do camarada B",
          partido: "PR/PE",
          imagem: "http://www.camara.gov.br/internet/deputado/bandep/178957.jpg"
        }
      ];
    });
})();
