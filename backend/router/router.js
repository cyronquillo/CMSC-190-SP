'use strict';


const controller = require(__dirname + '/../controller/controller');



module.exports = (router) => {
    router.get('/api/get-score/:sentences', controller.get_score);
    router.get('/api/parse-sentences/:sentences', controller.parse_sentences);
    router.get('/api/get-sentence-relevance-score/:sentences', controller.get_sentence_relevance_score);
    router.get('/api/get-sentence-certainty-score/:sentences', controller.get_sentence_certainty_score);

    router.all('*', (req, res, next) => {
        res.status(404).send({
            'message': 'Not Found!'
        });
    });

    return router;
}
