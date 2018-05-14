'use strict';

(() => {
    angular
        .module('app')
        .factory('MainService', MainService);

    MainService.$inject = ['$window', '$http', '$q', '$httpParamSerializer'];

    const headers = {
        'content': 'application/x-www-form-urlencoded'
    };

    function MainService($window, $http, $q, $httpParamSerializer) {


        const get_scores = (data) => {
            let deferred = $q.defer();
            $http({
                method: 'GET',
                data: $httpParamSerializer(data),
                url: '/api/get-score/' + data.sentences,
                headers: headers
            })
                .then(function (res) {
                    deferred.resolve(res.data);
                }, function (err) {
                    console.log(err);
                    deferred.reject(err.data);
                })
            return deferred.promise;
        }

        const parse_sentences = (data) => {
            let deferred = $q.defer();
            $http({
                method: 'GET',
                data: $httpParamSerializer(data),
                url: '/api/parse-sentences/' + data.sentences,
                header: headers
            })
                .then(function(res) {
                    deferred.resolve(res.data);   
                }, function (err) {
                    console.log(err);
                    deferred.reject(err.data);
                })
            return deferred.promise;
        }

        const get_sentence_relevance_score = (data) => {
            let deferred = $q.defer();
            $http({
                method: 'GET',
                data: $httpParamSerializer(data),
                url: '/api/get-sentence-relevance-score/' + data.sentences,
                header: headers
            })
                .then(function (res) {
                    deferred.resolve(res.data);
                }, function (err) {
                    console.log(err);
                    deferred.reject(err.data);
                })
            return deferred.promise;
        }

        const get_sentence_certainty_score = (data) => {
            let deferred = $q.defer();
            $http({
                method: 'GET',
                data: $httpParamSerializer(data),
                url: '/api/get-sentence-certainty-score/' + data.sentences,
                header: headers
            })
                .then(function (res) {
                    console.log(res.data)
                    deferred.resolve(res.data);
                }, function (err) {
                    console.log(err);
                    deferred.reject(err.data);
                })
            return deferred.promise;
        }


        let service = {
            get_scores: get_scores,
            parse_sentences: parse_sentences,
            get_sentence_relevance_score: get_sentence_relevance_score,
            get_sentence_certainty_score: get_sentence_certainty_score

        };

        return service;
    }


})();