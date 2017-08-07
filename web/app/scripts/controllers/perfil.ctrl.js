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
      vm.contagemSelos = {
        'Divulgação de atividade parlamentar': 0,
        'Combustíveis': 0,
        'Alimentação': 0,
        'Escritório': 0,
        'Locação de veículos': 0,
        'Passagens aéreas': 0,
        'moderado': 0,
        'camarote': 0,
        'batedor': 0,
        'gaspar': 0
      }

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
          contaSelos(vm.selos);
        });

        $http.get(RESTAPI+"selosCotaPresenca/"+vm.id).then(function(res) {
          vm.selosCotaPresenca = res.data;
          contaSelos(vm.selosCotaPresenca);
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

      function contaSelos(selos) {
        for (var i in selos) {
          if (selos[i][3] != '-') {
            vm.contagemSelos[selos[i][3]] = vm.contagemSelos[selos[i][3]] + 1;
          }
        }
      };

    });
})();
