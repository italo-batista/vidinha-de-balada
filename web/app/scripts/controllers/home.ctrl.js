(function () {
    'use strict';

    angular
        .module('baladaApp')
        .controller('HomeCtrl', function ($http, RESTAPI) {
            var vm = this;
            vm.total = 0;
            vm.salariosMinimos = 0;
            vm.casasPopulares = 0;
            vm.cestasBasicas = 0;
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

            // Os valores medianos de casasPopulares e cestasBasicas foram calculados com base em
            // http://g1.globo.com/economia/noticia/governo-amplia-minha-casa-minha-vida-para-familias-com-renda-de-ate-r-9-mil.ghtml
            // e https://www.dieese.org.br/analisecestabasica/2017/201705cestabasica.pdf
            function setAno(ano) {
                vm.anoSelecionado = ano;
                $http.get(RESTAPI + "gasto_anual?ano=" + vm.anoSelecionado).then(function (res) {
                    vm.total = res.data[0];
                    vm.salariosMinimos = Math.round(vm.total / 937000);
                    vm.casasPopulares = Math.round(vm.total / 152500);
                    vm.cestasBasicas = Math.round(vm.total / 390600);
                    setTextosEquivalentes(vm.salariosMinimos, vm.casasPopulares, vm.cestasBasicas);
                });
            };

            function subirAno() {
                if (vm.anoSelecionado < vm.anoMaximo) {
                    setAno(vm.anoSelecionado + 1)
                }
            }

            function descerAno() {
                if (vm.anoSelecionado > vm.anoMinimo) {
                    setAno(vm.anoSelecionado - 1)
                }
            }

            function isPossivelSubir() {
                return vm.anoSelecionado >= vm.anoMaximo;
            }

            function isPossivelDescer() {
                return vm.anoSelecionado <= vm.anoMinimo;
            }

            function setTextosEquivalentes(salariosMinimos, casasPopulares, cestasBasicas) {
              vm.textosEquivalentes = [
                {
                  texto: "milhões de salários mínimos",
                  valor: salariosMinimos
                },
                {
                  texto: "mil casas populares",
                  valor: casasPopulares
                },
                {
                  texto: "milhões de cestas básicas",
                  valor: cestasBasicas
                }
              ];
            }

            function init() {
                setAno(vm.anoMaximo);
                $http.get(RESTAPI + "top10").then(function (res) {
                    res.data.forEach(function (d) {
                        d.nome = d.nome.replace('"', '').replace('\"', '');
                        d.uf = d.uf.replace('"', '').replace('\"', '');

                        if (d.urlfoto === "NA") {
                            d.urlfoto = "http://www.camara.leg.br/internet/deputado/bandep/" + d.id + ".jpg";
                        } else {
                            d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
                        }

                        vm.deputados.push(d);
                    })
                });
            }

            init();

        });
})();
