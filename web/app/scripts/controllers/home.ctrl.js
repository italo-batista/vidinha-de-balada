(function () {
    'use strict';

    angular
        .module('baladaApp')
        .controller('HomeCtrl', function ($http, RESTAPI, UFs) {
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
            vm.mesTop10 = 0;
            vm.anoTop10 = 0;
            vm.showTop10 = 0;
            vm.rankingSelecionado = 'geral';
            vm.ufSelecionada = '--';
            vm.partidoSelecionado = '--';
            vm.ufs = UFs;
            vm.exibirTop10 = exibirTop10;
            vm.setAno = setAno;
            vm.subirAno = subirAno;
            vm.descerAno = descerAno;
            vm.isPossivelSubir = isPossivelSubir;
            vm.isPossivelDescer = isPossivelDescer;
            vm.pesquisarGeral = pesquisarGeral;
            vm.pesquisarPorEstado = pesquisarPorEstado;
            vm.pesquisarPorPartido = pesquisarPorPartido;

            function init() {
                setAno(vm.anoMaximo);
                $http.get(RESTAPI + "top10").then(function (res) {
                    res.data.forEach(function (d) {
                        d.nome = d.Nome.replace('"', '').replace('\"', '');
                        d.uf = d.UF.replace('"', '').replace('\"', '');

                        if (d.urlfoto === "NA") {
                            d.urlfoto = "http://www.camara.leg.br/internet/deputado/bandep/" + d.id + ".jpg";
                        } else {
                            d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
                        }

                        vm.deputados.push(d);
                    });
                    vm.showTop10++;
                });
                $http.get(RESTAPI + "dadosData").then(function(res) {
                  vm.mesTop10 = res.data.mes;
                  vm.anoTop10 = res.data.ano;
                  vm.showTop10++;
                });
            }
            init();

            // Os valores medianos de casasPopulares e cestasBasicas foram calculados com base em
            // http://g1.globo.com/economia/noticia/governo-amplia-minha-casa-minha-vida-para-familias-com-renda-de-ate-r-9-mil.ghtml
            // e https://www.dieese.org.br/analisecestabasica/2017/201705cestabasica.pdf
            function setAno(ano) {
                vm.anoSelecionado = ano;
                $http.get(RESTAPI + "gastometro/" + vm.anoSelecionado).then(function (res) {
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

            function exibirTop10() {
              return vm.showTop10 >= 2;
            }

            function pesquisarGeral() {
              if (vm.rankingSelecionado === 'geral') {
                vm.deputados = [];
                $http.get(RESTAPI + "top10").then(function (res) {
                  res.data.forEach(function (d) {
                    d.nome = d.Nome.replace('"', '').replace('\"', '');
                    d.uf = d.UF.replace('"', '').replace('\"', '');

                    if (d.urlfoto === "NA") {
                      d.urlfoto = "http://www.camara.leg.br/internet/deputado/bandep/" + d.id + ".jpg";
                    } else {
                      d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
                    }

                    vm.deputados.push(d);
                  });
                  vm.ufSelecionada = '--';
                  vm.partidoSelecionado = '--';
                });
              }
            }

            function pesquisarPorEstado() {
              vm.deputados = [];
              $http.get(RESTAPI + "top10/uf/"+vm.ufSelecionada).then(function(res) {
                  res.data.forEach(function (d) {
                      d.nome = d.Nome.replace('"', '').replace('\"', '');
                      d.uf = d.UF.replace('"', '').replace('\"', '');
                      if (d.urlfoto === "NA") {
                          d.urlfoto = "http://www.camara.leg.br/internet/deputado/bandep/" + d.id + ".jpg";
                      } else {
                          d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
                      }
                      vm.deputados.push(d);
                  });
              });
            }

            function pesquisarPorPartido() {
              vm.deputados = [];
              $http.get(RESTAPI + "top10/partido/"+vm.partidoSelecionado).then(function(res) {
                  res.data.forEach(function (d) {
                      d.nome = d.Nome.replace('"', '').replace('\"', '');
                      d.uf = d.UF.replace('"', '').replace('\"', '');
                      if (d.urlfoto === "NA") {
                          d.urlfoto = "http://www.camara.leg.br/internet/deputado/bandep/" + d.id + ".jpg";
                      } else {
                          d.urlfoto = d.urlfoto.replace('"', '').replace('\"', '');
                      }
                      vm.deputados.push(d);
                  });
              });
            }

            $(document).ready(function () {
              var menu = $('.menu');
              var origOffsetY = menu.offset().top;

              function scroll() {
                  if ($(window).scrollTop() >= origOffsetY) {
                      $('.menu').addClass('navbar-fixed-top');
                  } else {
                      $('.menu').removeClass('navbar-fixed-top');
                  }
              }
              document.onscroll = scroll;
            });

        });
})();
