'use strict';
var app = angular.module('baladaApp');

app.directive('lineChart', function ($parse) {
    var directiveDefinitionObject = {
        restrict: 'E',
        replace: false,
        link: function (scope, element, attrs) {

            var width = 500,
                height = 300;
            var margin = {top: 20, right: 80, bottom: 30, left: 50};

            var chart = d3.select("#line-chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);

            var g = chart.append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var x = d3.scaleTime().range([0, width]),
                y = d3.scaleLinear().range([height, 0]);

            var color = d3.scaleOrdinal(d3.schemeCategory10)

            var line = d3.line()
                .curve(d3.curveBasis)
                .x(function (d) {
                    return x(d.date);
                })
                .y(function (d) {
                    return y(+d.total);
                });

            d3.csv("data/mais_dps_2016.csv", function (error, data) {
                if (error) throw error;

                var parseTime = d3.timeParse("%m %Y");
                data.forEach(function (d) {
                    d.date = parseTime(d.mes + " " + d.ano);
                });

                x.domain(d3.extent(data, function (d) {
                    return d.date;
                }));

                color.domain(d3.extent(data, function (d) {
                    return d.txNameParlamentar;
                }));

                y.domain([
                    d3.min(data, function (c) {
                        return +c.total;
                    }),
                    d3.max(data, function (c) {
                        return +c.total;
                    })
                ]);

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

                var politico = g.selectAll(".politico")
                    .data(data)
                    .enter().append("g")
                    .attr("class", "politico");

                politico.append("path")
                    .datum(data.filter( function (p) {
                        return p.txNomeParlamentar === "DELEGADO WALDIR"
                    }))
                    .attr("data-legend", "Min")
                    .attr("class", "line")
                    .attr("d", line)
                    .style("stroke", "#2196F3");

                politico.append("path")
                    .datum(data.filter( function (p) {
                        return p.txNomeParlamentar === "JÚLIO DELGADO"
                    }))
                    .attr("data-legend", "Med")
                    .attr("class", "line")
                    .attr("d", line)
                    .style("stroke", "#F06292");

                politico.append("path")
                    .datum(data.filter( function (p) {
                        return p.txNomeParlamentar === "ABEL MESQUITA JR."
                    }))
                    .attr("data-legend", "Max")
                    .attr("class", "line")
                    .attr("d", line)
                    .style("stroke", "#F44336");

                politico.append("text")
                    .attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(+d.total) + ")"; })
                    .attr("x", 3)
                    .attr("dy", "0.35em")
                    .style("font", "10px sans-serif");

            });
        }
       };
     return directiveDefinitionObject;
  });
