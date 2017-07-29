(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('PerfilCtrl', function($http, $stateParams, RESTAPI) {
      var vm = this;
      vm.deputado = {}
      vm.id = $stateParams.id;

      function init() {
        $http.get(RESTAPI+"deputado?id="+vm.id).then(function(res) {
          vm.deputado = res.data;
          vm.deputado.nome = vm.deputado.Nome.replace('"', '').replace('\"', '');
          vm.deputado.urlfoto = vm.deputado.urlfoto.replace('"', '').replace('\"', '');
        });
      }
      init();
    });
})();
