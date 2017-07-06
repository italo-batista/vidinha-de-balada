(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('HomeCtrl', function($http, RESTAPI) {
      var vm = this;
      vm.total = 0;
      vm.salariosMinimos = 0;
      vm.deputados = [];
      vm.textosEquivalentes = [];
      vm.anoSelecionado = 0;
      vm.anoMaximo = new Date().getFullYear();
      vm.anoMinimo = 2015;
      vm.setAno = setAno;
      vm.subirAno = subirAno;
      vm.descerAno = descerAno;
      vm.isPossivelSubir = isPossivelSubir;
      vm.isPossivelDescer = isPossivelDescer;

      function setAno(ano) {
        vm.anoSelecionado = ano;
        $http.get(RESTAPI+"gasto_anual?ano="+ vm.anoSelecionado).then(function(res) {
          vm.total = res.data[0];
          vm.salariosMinimos = Math.round( vm.total / 937000);
          setTextosEquivalentes(vm.salariosMinimos);
        });
      };

      function subirAno() {
        if (vm.anoSelecionado < vm.anoMaximo) {
          setAno(vm.anoSelecionado+1)
        }
      }

      function descerAno() {
        if (vm.anoSelecionado > vm.anoMinimo) {
          setAno(vm.anoSelecionado-1)
        }
      }

      function isPossivelSubir() {
        return vm.anoSelecionado >= vm.anoMaximo;
      }

      function isPossivelDescer() {
        return vm.anoSelecionado <= vm.anoMinimo;
      }

      function setTextosEquivalentes(salariosMinimos) {
        vm.textosEquivalentes = [
          {
            texto: "milhões de salários mínimos",
            valor: salariosMinimos
          },
          {
            texto: "mil casas populares",
            valor: salariosMinimos
          },
          {
            texto: "milhões de cestas básicas",
            valor: salariosMinimos
          }
        ];
      }

      function init() {
        setAno(vm.anoMaximo);
        $http.get(RESTAPI+"top10").then(function(res) {
          res.data.forEach(function(d) {
            d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
            d.nome = d.nome.replace('"', '').replace('\"', '');
            d.uf = d.uf.replace('"', '').replace('\"', '');
            vm.deputados.push(d);
          })
        });
      }

      init();

    });
})();
