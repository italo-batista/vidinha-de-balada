'use strict';
var app = angular.module('baladaApp');

app.directive('lineChart', function ($parse, $window) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: false,
        link: function (scope, element, attrs) {
          var width = 1000,
			        height = 500;
          var chart = d3.select("#line-chart")
            .append("svg")
              .attr('version', '1.1')
              .attr('viewBox', '0 0 '+width+' '+height)
              .attr('width', '100%');
          var margin = {top: 20, right: 80, bottom: 30, left: 50};
          var width = width - margin.left - margin.right;
          var height = height - margin.top - margin.bottom;
          var g = chart.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          var x = d3.scaleTime().range([0, width]),
              y = d3.scaleLinear().range([height, 0]),
              z = d3.scaleOrdinal(d3.schemeCategory10);

          var line = d3.line()
              .x(function(d) { return x(d.date); })
              .y(function(d) { return y(+d.total); })

          d3.csv("data/mais_dps_2016.csv", function(error, data) {
            if (error) throw error;

            var parseTime = d3.timeParse("%m %Y");
            data.forEach(function(d) {
              d.date = parseTime(d.mes + " " + d.ano);
            });

            x.domain(d3.extent(data, function(d) { return d.date; }));

            y.domain([
              d3.min(data, function(c) { return +c.total; }),
              d3.max(data, function(c) { return +c.total; })
            ]);

            z.domain(data.map(function(c) { return c.txNomeParlamentar; }));

            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y))
              .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", "0.71em")
                .attr("fill", "#000")
                .text("Gasto total, R$");

            var city = g.selectAll(".city")
              .data(data)
              .enter().append("g")
                .attr("class", "city");

            city.append("path")
              .datum(data)
                .attr("class", "line")
                .attr("d", line)
                .style("stroke", function(d) { return z(d.txNomeParlamentar); });

              city.append("text")
                  .attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(+d.total) + ")"; })
                  .attr("x", 3)
                  .attr("dy", "0.35em")
                  .style("font", "10px sans-serif");
          });

        }
       };
     return directiveDefinitionObject;
  });
