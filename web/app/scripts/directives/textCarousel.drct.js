(function() {
    'use strict';

    angular.module('baladaApp')
        .directive('vbTextCarousel', ['$timeout', vbTextCarousel]);


    /*jshint latedef: nofunc */
    function vbTextCarousel($timeout) {
        return {
            restrict: 'A',
            scope: {
              carouselItems: '=',
              interval: '='
            },
            link: function (scope, elem, attrs) {
              var timeoutId, index = 0;

              function setCarouselText() {
                if (scope.carouselItems.length > 0) {
                  elem.html('<strong>'+scope.carouselItems[index].valor+'<strong> '+scope.carouselItems[index].texto);
                }
              }

              function goToNextValue() {
                index += 1;
                if (index >= scope.carouselItems.length) {
                  index = 0;
                }
              };

              function scheduleNext() {
                timeoutId = $timeout(function () {
                  elem.fadeOut(scope.interval/50, function () {
                    $(this).html('<strong>'+scope.carouselItems[index].valor+'<strong> '+scope.carouselItems[index].texto).fadeIn(scope.interval/10);
                    updateCarousel();
                  });
                }, scope.interval);
              };

              function updateCarousel() {
                setCarouselText();
                goToNextValue();
                scheduleNext();
              };

              updateCarousel();

              elem.on('$destroy', function () {
                $timeout.cancel(timeoutId);
            });
          }
        };
    }



})();
