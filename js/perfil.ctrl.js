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
          console.log(res.data);
          vm.deputado = res.data;
        })
      }
      init();
    });
})();
