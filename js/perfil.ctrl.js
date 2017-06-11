(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('PerfilCtrl', function() {
      var vm = this;
      vm.deputado = {
        nome: "Nome do camarada",
        partido: "PR/PB",
        imagem: "http://www.camara.gov.br/internet/deputado/bandep/178957.jpg"
      }
    });
})();
