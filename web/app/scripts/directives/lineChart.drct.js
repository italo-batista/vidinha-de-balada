'use strict';
var app = angular.module('baladaApp');

app.directive('lineChart', function ($parse, RESTAPI) {
  var directiveDefinitionObject = {
    restrict: 'E',
    replace: false,
    scope: {
      deputado: '='
    },
    link: function (scope, element, attrs) {
      var width = 1000,
          height = 600;
      var margin = {top: 20, right: 80, bottom: 30, left: 100};

      var chart = d3.select("#line-chart")
        .append("svg")
        .attr('version', '1.1')
        .attr('viewBox', '0 0 '+(width + margin.left + margin.right)+' '+(height + margin.top + margin.bottom))
        .attr('width', '100%');

      var g = chart.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var x = d3.scaleTime().range([0, width]),
          y = d3.scaleLinear().range([height, 0]);

      var line = d3.line()
        .curve(d3.curveBasis)
        .x(function (d) { return x(d.date); })
        .y(function (d) { return y(+d.total); });

      d3.json(RESTAPI+"timeline?id="+scope.deputado, function (error, data) {
        if (error) throw error;

        var parseTime = d3.timeParse("%m/%Y");
        data.forEach(function (d) {
          d.date = parseTime(Object.keys(d)[0]);
          d.valor = +d[Object.keys(d)[0]]
        });

        x.domain(d3.extent(data, function (d) {
          return d.date;
        }));

        y.domain([
          d3.min(data, function (c) {
            return +c.valor;
          }),
          d3.max(data, function (c) {
            return +c.valor
          })
        ]);

        var line = d3.line()
          .x(function(d) { return x(d.date); })
          .y(function(d) { return y(d.valor); });

        g.append("path")
          .datum(data)
          .attr("fill", "None")
          .attr("stroke", "#ff4e81")
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 2)
          .attr("d", line);

        g.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%m/%Y")));

        g.append("g")
          .attr("class", "axis axis--y")
          .style("font", "14px sans-serif")
          .call(d3.axisLeft(y))
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", "0.71em")
          .attr("fill", "#000")
          .text("Gasto total mensal, R$");
        })
      }
    }
    return directiveDefinitionObject;
  });
