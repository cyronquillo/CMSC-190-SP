'use strict';

const PythonShell = require('python-shell');

const winston = require('winston');
const child_process = require('child_process');

exports.get_score = (req, res, next) => {
    const payload = [req.params.word]; 

    const spawn = child_process.spawn;
    const process = spawn("python", ["../api/api.py", 
        payload[0]
    ]);

    process.stdout.on("data", function (data){
        res.status(200).send(data.toString());
    });
}


exports.parse_sentences = (req, res, next) => {
    console.log("inside backend parse_sentences")
    console.log("backend->controller: "+req.params.sentences)
    var payload = {
        pythonPath:'python3.5',
        args:
        [
            req.params.sentences
        ]
    }

    PythonShell.run('./api/sentence_tokenize.py', payload, function (err, data){
        if(err){
            res.status(404).send(err);
        } else {
            res.send(data.toString())
        }
    })
}

exports.get_sentence_relevance_score = (req, res, next) => {
    req.setTimeout(0);
    var payload = {
        pythonPath:'python3.5',
        args: [req.params.sentences]
    }

    PythonShell.run('./api/sentence_classification/sentence_classifier.py', payload, function (err, data) {
        if (err) {
            console.log(err)
            res.status(404).send(err);
        } else {
            console.log(data.toString())
            res.send(data.toString())
        }
    })
}


exports.get_sentence_certainty_score = (req, res, next) => {
    req.setTimeout(0);
    var payload = {
        pythonPath:'python3.5',
        args: [req.params.sentences]
    }
    console.log(req.params.sentences)
    PythonShell.run('./api/semantic_similarity_analysis/sentence_scorer.py', payload, function (err, data) {
        if (err) {
            console.log(err)
            res.status(404).send(err);
        } else {
            console.log(data.toString())
            res.status(200).send(data.toString())
        }
    })
}
