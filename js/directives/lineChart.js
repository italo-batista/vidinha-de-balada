'use strict';
var app = angular.module('baladaApp');

app.directive('lineChart', function ($parse, $window) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: false,
        link: function (scope, element, attrs) {
          var width = 1000,
			        height = 500;
          var chart = d3.select("#barchart")
            .append("svg")
              .attr('version', '1.1')
              .attr('viewBox', '0 0 '+width+' '+height)
              .attr('width', '100%');
          var margin = {top: 20, right: 80, bottom: 30, left: 50};
          var width = width - margin.left - margin.right;
          var height = height - margin.top - margin.bottom;
          var g = chart.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var parseTime = d3.timeParse("%m/%Y");

        var x = d3.scaleTime().range([0, width]),
            y = d3.scaleLinear().range([height, 0]),
            z = d3.scaleOrdinal(d3.schemeCategory20);

        var line = d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.total); });

        d3.csv("data/gasto_mensal_por_depoutado_por_categoria.csv", type, function(error, data) {
          if (error) throw error;

          var gastoTotal = d3.nest()
            .key(function(d) {return (d.txNomeParlamentar + " " + d.mes + "/" + d.ano);})
            .rollup(function(d) {
              return d3.sum(d, function(g) {return +g.total; });
            }).entries(data);
            data.forEach(function(d) {
             d.date = d.key;
             d.value = d.values;
            });

            gastoTotal.forEach(function(d) {
             d.date = d.key.split(" ").slice(-1)[0];
             d.nome = d.key.replace(d.date, "").trim();
             d.total = d.value;
            });
          console.log('%%%%%%%', gastoTotal)
          x.domain(d3.extent(gastoTotal, function(d) { return d.date; }));

          y.domain([
            d3.min(gastoTotal, function(c) { return c.total; }),
            d3.max(gastoTotal, function(c) { return c.total; })
          ]);

          z.domain(gastoTotal.map(function(c) { return c.nome; }));
          console.log('&&&&&&&&&');
          g.append("g")
              .attr("class", "axis axis--x")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x));
          console.log('%%%%%%%%%%%%');
          g.append("g")
              .attr("class", "axis axis--y")
              .call(d3.axisLeft(y))
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", "0.71em")
              .attr("fill", "#000")
              .text("Gasto total, R$");
          console.log('***********')
          var city = g.selectAll(".city")
            .data(gastoTotal)
            .enter().append("g")
              .attr("class", "city");

          city.append("path")
              .attr("class", "line")
              .attr("d", function(d) { return line({"total": d.total, "date":d.date}); })
              .style("stroke", function(d) { return z(d.nome); });

          city.append("text")
              .datum(function(d) { return {nome: d.nome, total: d.total}; })
              .attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(d.total) + ")"; })
              .attr("x", 3)
              .attr("dy", "0.35em")
              .style("font", "10px sans-serif")
              .text(function(d) { return d.nome; });
        });

        function type(d, _, columns) {
          d.date = parseTime(d.date);
          for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
          return d;
        }
      }
     };
     return directiveDefinitionObject;
  });
