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
        $scope.mode = undefined;
        $scope.submitted_mode = undefined;
        $scope.list = [
            {
                sentence:"-",
                sentence_certainty:"-",
                sentence_relevance:"-",
                editable: false,
                is_done: false
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
                        sentence_relevance: "-",
                        editable: false,
                        is_done: false
                    }
                )
            }
            if ($scope.submitted_mode == "gts" || $scope.submitted_mode == "gcs")
                $scope.get_sentence_certainty_score();
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
            console.log(obj)
            
            for(var i = 0; i < Object.keys(obj.scores).length; i++){
                $scope.list[i].sentence_relevance = obj.scores[i];
                if($scope.submitted_mode != "gts"){
                    $scope.list[i].is_done = true;
                }
            }
            if($scope.submitted_mode == "gts") $scope.compute_transcript_score();
            else {
                NProgress.done()
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
            console.log(obj)
            console.log("storing");
            console.log(obj.scores[0])
            for (var i = 0; i < Object.keys(obj.scores).length; i++) {
                $scope.list[i].sentence_certainty = obj.scores[i];
                if ($scope.submitted_mode != "gts") {
                    $scope.list[i].is_done = true;
                }
            }
            if ($scope.submitted_mode == "gts") $scope.compute_transcript_score();
            else {
                NProgress.done()
            }
        }

        $scope.compute_transcript_score = function () {
            $scope.transcript_score = 0
            for(var i = 0; i < $scope.list.length; i++){
                $scope.transcript_score += 
                    ($scope.list[i].sentence_certainty * $scope.list[i].sentence_relevance)
                $scope.list[i].is_done = true;
            }
            $scope.transcript_score /= $scope.list.length
            console.log($scope.transcript_score);
            
            if (isNaN($scope.transcript_score)){
                $scope.transcript_score = undefined
                if($scope.submitted_mode == "gts") NProgress.set(0.5);
            }
            if (!isNaN($scope.transcript_score)) {
                $scope.transcript_score = ($scope.transcript_score).toFixed(4);
                NProgress.done();
            }
        }

        $scope.modify_sentence = function(index) {
            var change = document.getElementById(index).isContentEditable;
            var elem = document.getElementById(index);
            var button1 = document.getElementById("edit" + index);
            var button2 = document.getElementById("delete" + index);
            if(change){
                // to save
                button1.innerText = "Edit"
                button2.innerText = "Delete"
                $scope.list[index].sentence = elem.innerText;

                $scope.update_scores(index);
            } else{
                // to start editing
                button1.innerText = "Save"
                button2.innerText = "Cancel"
            }
            elem.contentEditable = !change;
            $scope.list[index].editable = !change;
            elem.focus();
            console.log($scope.list)
        }

        $scope.update_scores = function (index) {
            var srs = document.getElementById("srs" + index)
            var scs = document.getElementById("scs" + index)
            if (($scope.submitted_mode == "gts" || $scope.submitted_mode == "grs") && srs.classList.length == 4){
                $scope.list[index].is_done = false;
                MainService
                .get_sentence_relevance_score(
                    { sentences: $scope.list[index].sentence }
                ).then(function (res) {
                    console.log(res);
                    var obj = { res }
                    $scope.list[index].sentence_relevance = obj.res[0];
                    $scope.compute_transcript_score();
                    $scope.list[index].is_done = true;
                }, function (err) {
                    console.log(err);
                })
            }
            if (($scope.submitted_mode == "gts" || $scope.submitted_mode == "gcs") && scs.classList.length == 4){
                $scope.list[index].is_done = false;
                MainService
                    .get_sentence_certainty_score(
                        { sentences: $scope.list[index].sentence }
                    ).then(function (res) {
                        var obj = { res }
                        console.log(res);
                        $scope.list[index].sentence_certainty = obj.res[0];
                        $scope.compute_transcript_score()
                        $scope.list[index].is_done = true;
                    }, function (err) {
                        console.log(err);
                    })
            }
        }


        $scope.delete_function = function(index) {
            var button1 = document.getElementById("edit" + index);
            var button2 = document.getElementById("delete"+index);
            if(button2.innerText == "Delete"){
                $scope.list.splice(index, 1);
                if ($scope.submitted_mode == 'gts')
                    $scope.compute_transcript_score()
            } else{
                // cancel
                var elem = document.getElementById(index);
                elem.innerText = $scope.list[index].sentence;
                button1.innerText = "Edit";
                button2.innerText = "Delete";
                elem.contentEditable = false;
                $scope.list[index].editable = false;
            }
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
        
        $scope.toggle = function(index) {
            var button = document.getElementById(index);
            button.classList.toggle("active");
        }
    }


};

mainCtrl();
