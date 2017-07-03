(function() {
    'use strict';

    angular.module('baladaApp')
        .directive('vbCountTo', ['$timeout', '$filter', vbCountTo]);


    /*jshint latedef: nofunc */
    function vbCountTo($timeout, $filter) {
        return {
            restrict: 'A',
            replace: false,
            scope: {},
            link: function(scope, element, attrs) {
                var e = element[0];
                var num, refreshInterval, duration, steps, step, countTo, value, increment;

                function calculate() {
                    refreshInterval = 20;
                    step = 0;
                    scope.timeoutId = null;
                    countTo = parseInt(attrs.countTo) || 0;
                    scope.value = parseInt(attrs.value, 10) || 0;
                    duration = (parseFloat(attrs.duration) * 1000) || 0;

                    steps = Math.ceil(duration / refreshInterval);
                    increment = ((countTo - scope.value) / steps);
                    num = scope.value;
                }

                function printOut() {
                    scope.timeoutId = $timeout(function () {
                        num += increment;
                        step++;
                        if (step >= steps) {
                            $timeout.cancel(scope.timeoutId);
                            num = countTo;
                            attrs.value = countTo;
                            e.textContent = $filter('currency')(countTo, 'R$ ');
                        } else {
                            e.textContent = $filter('currency')(Math.round(num), 'R$ ');
                            printOut();
                        }
                    }, refreshInterval);
                }

                function start() {
                    if (scope.timeoutId) {
                        $timeout.cancel(scope.timeoutId);
                    }
                    calculate();
                    printOut();
                }

                attrs.$observe('countTo', function (val) {
                    if (val) {
                        start();
                    }
                });

                attrs.$observe('value', function (val) {
                    start();
                });

                return true;
            }
        };
    }



})();
