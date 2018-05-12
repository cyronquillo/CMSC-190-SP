'use strict';



function mainCtrl() {
    angular
        .module('app')
        .controller('main-controller', main_controller);

    main_controller.$inject = ['$scope', '$location', 'MainService'];

    function main_controller($scope, $location, MainService) {
        $scope.sentences = undefined
        $scope.transcript_score = undefined
        $scope.button_status = "disabled";
        $scope.is_done = false;
        $scope.mode = undefined;
        $scope.submitted_mode = undefined;
        $scope.list = [
            {
                sentence:"-",
                sentence_certainty:"-",
                sentence_relevance:"-"
            }
        ]

        $scope.sliders = [
            {
                id:"gcs",
                label:"Get Certainty Score",
            },
            {
                id: "grs",
                label: "Get Relevance Score",
            },
            {
                id: "gts",
                label: "Get Transcript Score",
            }
        ]



        $scope.submit_sentences = function() {
            if($scope.sentences !== undefined && $scope.sentences !== ""){
                $scope.is_done = false
                $scope.submitted_mode = $scope.mode;
                NProgress.start();
                $scope.transcript_score = undefined
                MainService
                    .parse_sentences(
                        { sentences: $scope.sentences }
                    ).then(function (res) {
                        $scope.fill_list(res);
                    }, function (err) {
                        console.log(err);
                    })
            }
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
            if ($scope.submitted_mode == "gts" || $scope.submitted_mode == "gcs")
                $scope.get_sentence_certainty_score();
            else
                console.log("wtf imposible")
            if ($scope.submitted_mode == "gts" || $scope.submitted_mode == "grs")
                $scope.get_sentence_relevance_score();
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
            if($scope.submitted_mode == "gts") $scope.compute_transcript_score();
            else {
                NProgress.done()
                $scope.is_done = true;
            }
        }

        $scope.get_sentence_certainty_score = function() {
            console.log("getting certainty score");
            MainService
                .get_sentence_certainty_score(
                    { sentences: $scope.sentences }
                ).then(function (res) {
                    console.log(res);
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
                if ($scope.submitted_mode == "gts") $scope.compute_transcript_score();
                else {
                    NProgress.done()
                    $scope.is_done = true;
                }
        }

        $scope.compute_transcript_score = function () {
            $scope.transcript_score = 0
            for(var i = 0; i < $scope.list.length; i++){
                $scope.transcript_score += 
                    ($scope.list[i].sentence_certainty * $scope.list[i].sentence_relevance)
            }
            $scope.transcript_score /= $scope.list.length
            console.log($scope.transcript_score);
            
            if (isNaN($scope.transcript_score)){
                $scope.transcript_score = undefined
                NProgress.set(0.7);
            }
            if (!isNaN($scope.transcript_score)) {
                NProgress.done();
                $scope.is_done = true;
            }
        }

        $scope.modify_sentence = function(index) {
            console.log("Hello ");
        }

        $scope.remove_sentence = function(index) {
            $scope.list.splice(index, 1);
        }

        $scope.activate = function(id) {
            if (document.getElementById(id).checked){
                $scope.button_status = "enabled"
                for(var i = 0; i < $scope.sliders.length; i++){
                    if($scope.sliders[i].id == id){
                        $scope.mode = id
                    } else{
                        document.getElementById($scope.sliders[i].id).checked = false;
                    }
                }
            } else{
                $scope.button_status = "disabled";
                $scope.mode = "waley"
            }
            console.log($scope.mode)
        }
    }


};

mainCtrl();
