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

      var parseTime = d3.timeParse("%m/%Y");
      var formatTime = d3.timeFormat("%m/%Y");

      var x = d3.scaleTime().range([0, width]),
          y = d3.scaleLinear().range([height, 0]);
      var yp = d3.scaleLinear().range([height, 0]);

      var line = d3.line()
        .curve(d3.curveLinear)
        .x(function (d) { return x(d.date); })
        .y(function (d) { return y(+d.valor); });

      var gasto = d3.select("body").append("div")
        .attr("class", "tooltip_gasto")
        .style("opacity", 0);

      var presenca = d3.select("body").append("div")
        .attr("class", "tooltip_presenca")
        .style("opacity", 0);

      d3.json(RESTAPI+"timeline?id="+scope.deputado, function (error, data) {
        if (error) throw error;

        data.forEach(function (d) {
          d.date = parseTime(Object.keys(d)[0]);
          d.valor = +d[Object.keys(d)[0]][0];
          if (d[Object.keys(d)[0]].length > 1) {
            d.presenca = +d[Object.keys(d)[0]][1];
            d.presenca_string = d[Object.keys(d)[0]][2];
          }
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

        yp.domain([0, 1]);

        g.append("path")
          .datum(data)
          .attr("fill", "None")
          .attr("stroke", "#ff4e81")
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-width", 2)
          .attr("d", line)

        g.selectAll("presenca")
          .data(data.filter(function(d) {return d.presenca}))
          .enter().append("circle")
          .attr("r", 4)
          .attr("cx", function(d) { return x(d.date); })
          .attr("cy", function(d) { return yp(+d.presenca); })
          .attr("fill", "#fff")
          .on("mouseover", function(d) {
             presenca.transition()
               .duration(200)
               .style("opacity", 1);
             presenca.html("Presente em<br/>" + d.presenca_string + " votações<br/>" + formatTime(d.date))
               .style("left", (d3.event.pageX) + "px")
               .style("top", (d3.event.pageY - 30) + "px");
             })
           .on("mouseout", function(d) {
             presenca.transition()
               .duration(500)
               .style("opacity", 0);
             });

        g.selectAll("point")
          .data(data)
          .enter().append("circle")
          .attr("r", 3)
          .attr("cx", function(d) { return x(d.date); })
          .attr("cy", function(d) { return y(+d.valor); })
          .attr("fill", "transparent")
          .on("mouseover", function(d) {
             gasto.transition()
               .duration(200)
               .style("opacity", 1);
             gasto.html("R$" + d.valor  + "<br/>" + formatTime(d.date))
               .style("left", (d3.event.pageX) + "px")
               .style("top", (d3.event.pageY - 30) + "px");
             })
           .on("mouseout", function(d) {
             gasto.transition()
               .duration(500)
               .style("opacity", 0);
             });

        g.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%m/%Y")))
          .style("font-size", "16px");

        g.append("g")
          .attr("class", "axis axis--y")
          .style("font", "14px sans-serif")
          .call(d3.axisLeft(y).tickSize(0))
          .style("font-size", "16px")
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
