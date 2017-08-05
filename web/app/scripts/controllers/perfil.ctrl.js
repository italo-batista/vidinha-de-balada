(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('PerfilCtrl', function($http, $stateParams, RESTAPI) {
      var vm = this;
      vm.deputado = {};
      vm.empresasParceiras = [];
      vm.selos = [];
      vm.id = $stateParams.id;

      function init() {
        $http.get(RESTAPI+"deputados/"+vm.id).then(function(res) {
          vm.deputado = res.data;
          vm.deputado.nome = vm.deputado.Nome.replace('"', '').replace('\"', '');
          vm.deputado.urlfoto = vm.deputado.urlfoto.replace('"', '').replace('\"', '');
        });

        $http.get(RESTAPI+"empresasParceiras/"+vm.id).then(function(res) {
          vm.empresasParceiras = res.data;
        });

        $http.get(RESTAPI+"selosDeputado/"+vm.id).then(function(res) {
          vm.selos = res.data;
          console.log(vm.selos);
        });
      }
      init();

    });
})();
