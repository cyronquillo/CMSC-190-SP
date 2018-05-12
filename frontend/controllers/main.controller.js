'use strict';

function mainCtrl() {
    angular
        .module('app')
        .controller('main-controller', main_controller);

    main_controller.$inject = ['$scope', '$location', 'MainService'];

    function main_controller($scope, $location, MainService) {
        $scope.sentences = undefined
        $scope.list = [
            {
                sentence:"-",
                sentence_certainty:"-",
                sentence_relevance:"-"
            }
        ]

        $scope.submit_sentences = function() {
            
            if($scope.sentences !== undefined && $scope.sentences !== "")
            MainService
                .parse_sentences(
                    { sentences: $scope.sentences }
                ).then(function (res) {
                    $scope.fill_list(res);
                }, function (err) {
                    console.log(err);
                })
        }

        $scope.fill_list = function(sentences) {
            $scope.list = [];
            
            var obj = {sentences}            
            console.log(obj)
            for(var i = 0; i < Object.keys(obj.sentences).length; i++){
                $scope.list.push(
                    {
                        sentence: obj.sentences[i],
                        sentence_certainty: "-",
                        sentence_relevance: "-"
                    }
                )
            }

            $scope.get_sentence_relevance_score();
            $scope.get_sentence_certainty_score();
        }

        $scope.get_sentence_relevance_score = function() {
            console.log("getting relevance score");
            MainService
                .get_sentence_relevance_score(
                    { sentences: $scope.sentences }
                ).then(function (res) {
                    console.log(res);
                    $scope.store_sentence_relevance_score(res);
                }, function (err) {
                    console.log(err);
                })
        }

        $scope.store_sentence_relevance_score = function(scores) {
            var obj = {scores}
            console.log("storing");
            for(var i = 0; i < Object.keys(obj.scores).length; i++){
                $scope.list[i].sentence_relevance = obj.scores[i]
            }
        }

        $scope.get_sentence_certainty_score = function() {
            console.log("getting certainty score");
            MainService
                .get_sentence_certainty_score(
                    { sentences: $scope.sentences }
                ).then(function (res) {
                    console.log(res)
                    $scope.store_sentence_certainty_score(res);
                }, function (err) {
                    console.log(err);
                })
        }

        $scope.store_sentence_certainty_score = function (scores) {
            var obj = { scores }
            console.log("storing");
            for (var i = 0; i < Object.keys(obj.scores).length; i++) {
                $scope.list[i].sentence_certainty = obj.scores[i]
            }
        }


        $scope.modify_sentence = function(index) {
            console.log("Hello " + index);   
        }

        $scope.remove_sentence = function(index) {
            $scope.list.splice(index, 1);
        }
    }


};

mainCtrl();
