(function () {
    'use strict';

    angular.module('baladaApp')
        .factory('Categorias', categorias);

    categorias.$inject = [];

    function categorias() {
        var categorias = [
            "Alimentação",
            "Combustíveis",
            "Divulgação de atividade parlamentar",
            "Escritório",
            "Locação de veículos",
            "Passagens aéreas"
        ];
        return categorias;
    }
})();