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
      vm.contagemSelos = {
        'Divulgação de atividade parlamentar': 0,
        'Combustíveis': 0,
        'Alimentação': 0,
        'Escritório': 0,
        'Locação de veículos': 0,
        'Passagens aéreas': 0
      }

      function contaSelos() {
        for (var i in vm.selos) {
          vm.contagemSelos[vm.selos[i][3]] = vm.contagemSelos[vm.selos[i][3]] + 1;
        }
      };

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
          contaSelos();
        });
      }
      init();

    });
})();
