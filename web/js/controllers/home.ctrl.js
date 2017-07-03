(function() {
  'use strict';

  angular
    .module('baladaApp')
    .controller('HomeCtrl', function($http, RESTAPI) {
      var vm = this;
      vm.total = 0;
      vm.salariosMinimos = 0;

      vm.deputados = [];

      vm.selectedYear = new Date().getFullYear();
      vm.mandatoAnos = [0, 1, 2, 3].map(function (i) { return vm.selectedYear - i });

      vm.updateTotal = function () {
            $http.get(RESTAPI+"gasto_anual?ano="+ vm.selectedYear).then(function(res) {
                vm.total = res.data[0];
                vm.salariosMinimos = Math.round( vm.total / 937000);
            });
        };

      vm.getMes = function(mes) {
            mes = str(mes);
            switch (mes) {
                case "1":
                    return "Janeiro"
                    break;
                case "2":
                    return "Fevereiro"
                    break;
                case "3":
                    return "Março"
                    break;
                case "4":
                    return "Abril"
                    break;
                case "5":
                    return "Maio"
                    break;
                case "6":
                    return "Junho"
                    break;
                case "7":
                    return "Julho"
                    break;
                case "8":
                    return "Agosto"
                    break;
                case "9":
                    return "Setembro"
                    break;
                case "10":
                    return "Outubro"
                    break;
                case "11":
                    return "Novembro"
                    break;
                case "12":
                    return "Dezembro"
                    break;
                default:
                    return "--"
                    break;
            }
        };

      vm.setYear = function (y) {
            vm.selectedYear = y;
            vm.updateTotal();
        };

      function init() {
        vm.updateTotal();
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
