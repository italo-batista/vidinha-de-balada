'use strict';
var app = angular.module('baladaApp');

app.directive('radarChart', function ($parse) {
  var directiveDefinitionObject = {
      restrict: 'E',
      replace: false,
      scope: {
        deputado: '='
      },
      link: function (scope, element, attrs) {
        var id = scope.deputado;
        var dictCategoria = {
          'alimentacao': 'Alimentação',
          'locacao': 'Locação',
          'divulgacao': 'Divulgação',
          'passagem': 'Passagem',
          'combustivel': 'Combustível',
          'escritorio': 'Escritório',
        }
        var width = 700,
            height = 700;

        var config = {
            w: width,
            h: height,
            maxValue: 100,
            levels: 5,
            ExtraWidthX: 300
        }
        var svg = d3.select('#radar-chart')
          .append('svg')
            .attr('version', '1.1')
            .attr('viewBox', '0 0 '+width+' '+height)
            .attr('width', '100%');

        d3.json("data/todos.json", function(error, data) {
          if (error) throw error;
           var cfg = {
             radius: 5,
             w: 500,
             h: 500,
             factor: 1,
             factorLegend: 1,
             levels: 3,
             maxValue: 0,
             radians: 2 * Math.PI,
             opacityArea: 0.5,
             ToRight: 5,
             TranslateX: 80,
             TranslateY: 30,
             ExtraWidthX: 50,
             ExtraWidthY: 50,
             color: d3.scaleOrdinal().range(["#ff4e81", "#ff4e81"])
            };

          if('undefined' !== typeof options){
            for(var i in options){
              if('undefined' !== typeof options[i]){
                cfg[i] = options[i];
              }
            }
          }

          data = data[id];

          cfg.maxValue = 100;

          var allAxis = Object.keys(data);
          allAxis.splice(allAxis.indexOf("nome"), 1);
          allAxis.splice(allAxis.indexOf("total"), 1);
          var total = allAxis.length;
          var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
          var Format = d3.format('%');
          d3.select("#radar-chart").select("svg").remove();

          var g = d3.select("#radar-chart")
              .append("svg")
              .attr('version', '1.1')
              .attr('viewBox', '0 0 '+width+' '+height)
              .attr('width', '100%')
              .append("g")
              .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");

           var tooltip;

           //Circular segments
           for(var j=0; j<cfg.levels; j++){
             var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
             g.selectAll(".levels")
              .data(allAxis)
              .enter()
              .append("svg:line")
              .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
              .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
              .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
              .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
              .attr("class", "line")
              .style("stroke", "grey")
              .style("stroke-opacity", "0.75")
              .style("stroke-width", "0.3px")
              .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")");
           }

        var series = 0;

        var axis = g.selectAll(".axis")
            .data(allAxis)
            .enter()
            .append("g")
            .attr("class", "axis");

        axis.append("line")
          .attr("x1", cfg.w/2)
          .attr("y1", cfg.h/2)
          .attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
          .attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
          .attr("class", "line")
          .style("stroke", "grey")
          .style("stroke-width", "1px");

        axis.append("text")
          .attr("class", "legend")
          .text(function(d){return dictCategoria[d]})
          .style("font-family", "sans-serif")
          .style("font-size", "24px")
          .attr("text-anchor", "middle")
          .attr("dy", "1em")
          .attr("transform", function(d, i){return "translate(5, -15)"})
          .attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
          .attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});

        var dataValues = [];
        g.selectAll(".nodes").data(
          allAxis, function(x, y) {
            dataValues.push([
              cfg.w/2*(1-(parseFloat(Math.max((data[x]/data['total'])*100, 0))/cfg.maxValue)*cfg.factor*Math.sin(y*cfg.radians/total)),
              cfg.h/2*(1-(parseFloat(Math.max((data[x]/data['total'])*100, 0))/cfg.maxValue)*cfg.factor*Math.cos(y*cfg.radians/total))
            ]);
          }
        )
        dataValues.push(dataValues[0]);
        g.selectAll(".area")
          .data([dataValues])
            .enter()
            .append("polygon")
            .attr("class", "radar-chart-serie"+series)
              .style("stroke-width", "2px")
              .style("stroke", cfg.color(series))
                .attr("points",function(d) {
                  var str="";
                  for(var pti=0;pti<d.length;pti++){
                    str=str+d[pti][0]+","+d[pti][1]+" ";
                  }
                  return str;
                })
                 .style("fill", function(j, i){return cfg.color(series)})
                 .style("fill-opacity", cfg.opacityArea)
                 .on('mouseover', function (d){
                          var z = "polygon."+d3.select(this).attr("class");
                          g.selectAll("polygon")
                           .transition(200)
                           .style("fill-opacity", 0.1);
                          g.selectAll(z)
                           .transition(200)
                           .style("fill-opacity", .7);
                          })
                 .on('mouseout', function(){
                          g.selectAll("polygon")
                           .transition(200)
                           .style("fill-opacity", cfg.opacityArea);
                 });
          var tooltip = d3.select("body").append("div").attr("class", "toolTip");
          g.selectAll(".nodes")
              .data(allAxis).enter()
              .append("svg:circle")
              .attr("class", "radar-chart-serie"+series)
              .attr('r', cfg.radius)
              .attr("alt", function(j){return Math.max((data[j]/data['total'])*200, 0)})
              .attr("cx", function(j, i){
                return cfg.w/2*(1-(Math.max((data[j]/data["total"])*100, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
              })
              .attr("cy", function(j, i){
                return cfg.h/2*(1-(Math.max((data[j]/data["total"])*100, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
              })
              .attr("data-id", function(j){return j.area})
              .style("fill", "#fff")
              .style("stroke-width", "2px")
              .style("stroke", cfg.color(series)).style("fill-opacity", .9)
              .on('mouseover', function (d){
                    tooltip
                      .style("left", d3.event.pageX - 40 + "px")
                      .style("top", d3.event.pageY - 40 + "px")
                      .style("display", "inline-block")
                      .html(("R$ " + data[d]))
                      .style("font-size", "10px");
                    })
                .on("mouseout", function(d){ tooltip.style("display", "none");});

              series++;
        });
      }
    };
   return directiveDefinitionObject;
});
