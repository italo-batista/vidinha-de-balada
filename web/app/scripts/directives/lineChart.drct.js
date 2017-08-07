(function() {
  'use strict';
  angular
    .module('baladaApp')
    .directive('lineChart', function ($parse, RESTAPI) {
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

        var chart = d3.select("#timeline-chart")
          .append("svg")
          .attr('version', '1.1')
          .attr('viewBox', '0 0 '+(width + margin.left + margin.right)+' '+(height + margin.top + margin.bottom))
          .attr('width', '100%');

        var g = chart.append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var parseTime = d3.timeParse("%Y/%m");
        var formatTime = d3.timeFormat("%m/%Y");

        var x = d3.scaleTime().range([0, width]),
            y = d3.scaleLinear().range([height, 0]);

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

        d3.json(RESTAPI+"timelineDeputado/"+scope.deputado, function (error, data) {
          if (error) throw error;
          var cota_mensal;
          const salarioMinimo = 937;
          data.forEach(function (d) {
            if (d.valor != '-') {
              d.date = parseTime(d.data);
              d.valor = (+d.total_gasto)/salarioMinimo;
              if (d.sessoes_total != '-') {
                d.presenca = d.total_presenca/d.sessoes_total;
              }
              cota_mensal = (+d.cota)/salarioMinimo;
            }
          });

          data.sort(function(a,b){
            return b.date - a.date;
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

          var yp = d3.scaleLinear().range([height, 0]);
          yp.domain([0, 1]);

          var dataMin = d3.min(data, function (c) {return +c.date});
          var dataMax = d3.max(data, function (c) {return +c.date});

          g.append("g")
            .attr("class", "axis axis--y gastos")
            .style("font", "14px sans-serif")
            .call(d3.axisLeft(y).tickSize(0))
            .style("font-size", "16px")
            .style("font-family", "'Montserrat', sans-serif")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .text("Gasto total mensal, salários mínimos")
            .style("font-family", "'Montserrat', sans-serif");

          g.append("line")
            .style("stroke", "#fff")
            .attr("stroke-dasharray", "5, 10")
            .attr("x1", x(dataMin))
            .attr("y1", y(cota_mensal))
            .attr("x2", x(dataMax))
            .attr("y2", y(cota_mensal));

          g.append("text")
            .attr("y", y(cota_mensal)-5)
            .attr("x", function(){ return x(dataMax)-5})
            .attr('text-anchor', 'end')
            .attr("fill", "#fff")
            .attr("font-size", "15px")
            .attr("font-family", "'Montserrat', sans-serif")
            .text("Cota mensal");

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
            .attr("r", 13)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return yp(+d.presenca); })
            .attr("fill", "None")
            .attr("stroke-width", 0.8)
            .attr("stroke", "#FF9B27")

          g.selectAll("presenca")
            .data(data.filter(function(d) {return d.presenca}))
            .enter().append("text")
            .attr("x", function(d) { return x(d.date); })
            .attr("y", function(d) { return yp(+d.presenca); })
            .attr("text-anchor", "middle")
            .attr("dy", ".3em")
            .attr("fill", "#FF9B27")
            .style("font-size", "11px")
            .style("font-family", "'Montserrat', sans-serif")
            .style("cursor", "default")
            .text(function(d){return d.total_presenca + "/" + d.sessoes_total})
            .on("mouseover", function(d) {
               presenca.transition()
                 .duration(200)
                 .style("opacity", 1);
               presenca.html("Presente em<br/>" + d.total_presenca +
               "/" + d.sessoes_total +  " votações<br/>" + formatTime(d.date))
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
               gasto.html(d.valor.toFixed(0) + " salários mínimos<br/>" + formatTime(d.date))
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
            .call(d3.axisBottom(x).tickSize(0).tickFormat(d3.timeFormat("%m/%Y")))
            .style("font-size", "16px")
            .style("font-family", "'Montserrat', sans-serif");

          g.append("g")
            .attr("class", "axis axis--y presenca")
            .style("font", "14px sans-serif")
            .attr("transform", "translate( " + width + ", 0 )")
            .call(d3.axisRight(yp).tickSize(0).tickFormat(""))
            .style("font-size", "16px")
            .style("font-family", "'Montserrat', sans-serif")
            .append("text")
            .attr("transform", "rotate(270)")
            .attr("y", -20)
            .attr("x", -135)
            .attr("dy", "0.71em")
            .attr("fill", "#FF9B27")
            .text("Presença mensal")
            .style("font-family", "'Montserrat', sans-serif");
          });
        }
      }
      return directiveDefinitionObject;
    })
})();
