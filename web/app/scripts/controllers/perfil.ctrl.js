(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('PerfilCtrl', function($http, $stateParams, RESTAPI) {
      var vm = this;
      vm.deputado = {};
      vm.empresasParceiras = [];
      vm.selos = [];
      vm.socialshare = {
        title: '',
        longText: '',
        shortText: '',
        url: '',
        media: '',
        hashtags: ''
      }
      vm.id = $stateParams.id;
      vm.getCategoria = getCategoria;

      function init() {
        $http.get(RESTAPI+"deputados/"+vm.id).then(function(res) {
          vm.deputado = res.data;
          vm.deputado.nome = vm.deputado.Nome.replace('"', '').replace('\"', '');
          vm.deputado.urlfoto = vm.deputado.urlfoto.replace('"', '').replace('\"', '');

          // Configura os metadados de compartilhamento
          vm.socialshare.title = vm.deputado.nome+" no Vidinha de Balada";
          vm.socialshare.longText = "Veja os gastos da CEAP de "+vm.deputado.nome+" no Vidinha de Balada";
          vm.socialshare.shortText = vm.socialshare.longText;
          vm.socialshare.url = "http://vidinhadebalada.com/#!/perfil/"+vm.deputado.Id;
          vm.socialshare.media = "http://vidinhadebalada.com/images/mediashare.png";
          vm.socialshare.hashtags = "VidinhaDeBalada";
        });

        $http.get(RESTAPI+"empresasParceiras/"+vm.id).then(function(res) {
          vm.empresasParceiras = res.data;
        });

        $http.get(RESTAPI+"selosDeputado/"+vm.id).then(function(res) {
          vm.selos = res.data;
        });
      }
      init();

      function getCategoria(categoria) {
        var categorias = {
          'Divulgação de atividade parlamentar': 'divulgacao',
          'Combustíveis': 'combustivel',
          'Alimentação': 'alimento',
          'Escritório': 'escritorio',
          'Locação de veículos': 'locacao',
          'Passagens aéreas': 'passagem'
        }
        return categorias[categoria];
      }

    });
})();
