(function () {
    'use strict';

    angular
        .module('baladaApp')
        .controller('HomeCtrl', function ($http, RESTAPI, UFs, Categorias) {
            var vm = this;
            vm.total = 0;
            vm.totalPorEscrito = '';
            vm.salariosMinimos = 0;
            vm.casasPopulares = 0;
            vm.cestasBasicas = 0;
            vm.deputados = [];
            vm.textosEquivalentes = [];
            vm.textosEquivalentes2 = [];
            vm.anoSelecionado = 0;
            vm.anoMaximo = new Date().getFullYear();
            vm.anoMinimo = 2015;
            vm.mesTop10 = 0;
            vm.anoTop10 = 0;
            vm.showTop10 = 0;
            vm.rankingSelecionado = 'geral';
            vm.ufSelecionada = '--';
            vm.partidoSelecionado = '--';
            vm.categoriaSelecionada = '--';
            vm.ufs = UFs;
            vm.categorias = Categorias;
            vm.exibirTop10 = exibirTop10;
            vm.setAno = setAno;
            vm.subirAno = subirAno;
            vm.descerAno = descerAno;
            vm.isPossivelSubir = isPossivelSubir;
            vm.isPossivelDescer = isPossivelDescer;
            vm.pesquisarGeral = pesquisarGeral;
            vm.pesquisarPorEstado = pesquisarPorEstado;
            vm.pesquisarPorPartido = pesquisarPorPartido;
            vm.pesquisarPorCategoria = pesquisarPorCategoria;

            vm.pibics = 0;
            vm.mestrandos = 0;
            vm.doutorandos = 0;
            vm.posdoutorandos = 0;

            function init() {
                setAno(vm.anoMaximo - 1);
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

            // Os valores de bolsas da CAPES foram calculados com base em
            // http://www.capes.gov.br/acessoainformacao/perguntas-frequentes/bolsas-de-estudo/4914-posso-acumular-a-bolsa-da-capes-com-atividade-remunerada
            function setAno(ano) {
                vm.anoSelecionado = ano;
                $http.get(RESTAPI + "gastometro/" + vm.anoSelecionado).then(function (res) {
                    vm.total = res.data[0];
                    vm.salariosMinimos = Math.round(vm.total / 937000);
                    vm.casasPopulares = Math.round(vm.total / 152500);
                    vm.cestasBasicas = Math.round(vm.total / 390600);

                    vm.pibics = vm.total / 4800000;
                    vm.mestrandos = vm.total / 18000000;
                    vm.doutorandos = vm.total / 26400000;
                    vm.posdoutorandos = vm.total / 49200000;

                    vm.totalPorEscrito = valorPorEscrito()
                    setTextosEquivalentes(vm.salariosMinimos, vm.casasPopulares, vm.cestasBasicas, vm.pibics, vm.mestrandos, vm.doutorandos, vm.posdoutorandos);
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

            function setTextosEquivalentes(salariosMinimos, casasPopulares, cestasBasicas, pibics, mestrandos, doutorandos, posdoutorandos) {
              vm.textosEquivalentes = [
                {
                  texto: "mil salários mínimos",
                  valor: salariosMinimos
                },
                {
                  texto: "casas populares",
                  valor: casasPopulares
                },
                {
                  texto: "mil cestas básicas",
                  valor: cestasBasicas
                }
              ];
              if (posdoutorandos >= 0 && posdoutorandos <= 1) {
                var textoPosdoutorandos = "pós doutorandos por ano";
                posdoutorandos = posdoutorandos * 1000;
              } else {
                var textoPosdoutorandos = "mil pós doutorandos por ano";
              }
              vm.textosEquivalentes2 = [
                {
                  texto: "mil estudantes de Pibid por ano",
                  valor: Math.round(pibics)
                },
                {
                  texto: "mil mestrandos por ano",
                  valor: Math.round(mestrandos)
                },
                {
                  texto: "mil doutorandos por ano",
                  valor: Math.round(doutorandos)
                },
                {
                  texto: textoPosdoutorandos,
                  valor: Math.round(posdoutorandos)
                }
              ];
            }

            function valorPorEscrito() {
                var texto = '';
                var total = vm.total;
                var milhoes = Math.floor(total/1000000);
                total = total - milhoes*1000000;
                var milhares = Math.floor(total/1000);
                if (milhoes > 1) {
                    texto += milhoes + ' milhões ';
                } else if (milhoes === 1) {
                    texto += milhoes + ' milhão ';
                }
                // if (milhares >= 1) {
                //     texto += (milhoes >= 1 && 'e ') + milhares + ' mil reais';
                // } else {
                    texto += 'de reais para 513 deputados';
                // }
                return texto;
            }

            function exibirTop10() {
              return vm.showTop10 >= 2;
            }

            function pesquisarGeral() {
              if (vm.rankingSelecionado === 'geral') {
                vm.deputados = [];
                vm.showTop10 = 0;
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
                  vm.showTop10 = 2;
                });
              }
            }

            function pesquisarPorEstado() {
              vm.deputados = [];
              vm.showTop10 = 0;
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
                  vm.showTop10 = 2;
              });
            }

            function pesquisarPorPartido() {
              vm.deputados = [];
              vm.showTop10 = 0;
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
                  vm.showTop10 = 2;
              });
            }

            function pesquisarPorCategoria() {
                vm.deputados = [];
                vm.showTop10 = 0;
                $http.get(RESTAPI + "top10/categoria/"+vm.categoriaSelecionada).then(function(res) {
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
                    vm.showTop10 = 2;
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
