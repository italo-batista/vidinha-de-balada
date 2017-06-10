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

        var parseTime = d3.timeParse("%Y%m");

        var x = d3.scaleTime().range([0, width]),
            y = d3.scaleLinear().range([height, 0]),
            z = d3.scaleOrdinal(d3.schemeCategory20);

        var line = d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.gasto); });

        d3.csv("data/gasto_mensal_por_depoutado_por_categoria.csv", type, function(error, data) {
          if (error) throw error;

          var gastoTotal = d3.nest()
            .key(function(d) {return d.txNomeParlamentar;})
            .key(function(d) {return d.ano;})
            .key(function(d) {return d.mes;})
            .rollup(function(d) {
              return d3.sum(d, function(g) {return +g.total; });
            }).entries(data);
            data.forEach(function(d) {
             d.date = d.key;
             d.value = d.values;
            });
          console.log("$$$$$$", gastoTotal);
        //   x.domain(d3.extent(data, function(d) { return d.date; }));
        //
        //   y.domain([
        //     d3.min(cities, function(c) { return d3.min(c.values, function(d) { return d.temperature; }); }),
        //     d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.temperature; }); })
        //   ]);
        //
        //   z.domain(cities.map(function(c) { return c.id; }));
        //
        //   g.append("g")
        //       .attr("class", "axis axis--x")
        //       .attr("transform", "translate(0," + height + ")")
        //       .call(d3.axisBottom(x));
        //
        //   g.append("g")
        //       .attr("class", "axis axis--y")
        //       .call(d3.axisLeft(y))
        //     .append("text")
        //       .attr("transform", "rotate(-90)")
        //       .attr("y", 6)
        //       .attr("dy", "0.71em")
        //       .attr("fill", "#000")
        //       .text("Temperature, ºF");
        //
        //   var city = g.selectAll(".city")
        //     .data(cities)
        //     .enter().append("g")
        //       .attr("class", "city");
        //
        //   city.append("path")
        //       .attr("class", "line")
        //       .attr("d", function(d) { return line(d.values); })
        //       .style("stroke", function(d) { return z(d.id); });
        //
        //   city.append("text")
        //       .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
        //       .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
        //       .attr("x", 3)
        //       .attr("dy", "0.35em")
        //       .style("font", "10px sans-serif")
        //       .text(function(d) { return d.id; });
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
