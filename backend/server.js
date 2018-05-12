'use strict';

const express = require('express');
const winston = require('winston');
const body_parser = require('body-parser');
const config = require(__dirname + '/config/config');
const router = require(__dirname + '/router/router');


let start;
let app;
let handler;

start = () => {
    if(handler){
        handler.close();
    }

    app = express();
    winston.cli();

    winston.level = config.LOG_LEVEL || 'silly';
    winston.log('info', 'Starting', config.APP_NAME);

    // configuring express app
    app.set('case sensitive routing', true);
    app.set('x-powered-by', false);

    // other packages that is needed to make the app secured and stable
    winston.log('verbose', 'Binding 3rd-party middlewares');
    app.use(express.static(__dirname + '/../frontend/'));
    app.use(require('method-override')());
    app.use(body_parser.urlencoded({ extended: true }));
    app.use(body_parser.json());
    app.use(require('compression')());
    app.use(router(express.Router()));

    // this will start app
    winston.log('info', 'Server listening on port', config.PORT);
    return app.listen(config.PORT, config.IP);

}

handler = start();

module.exports = {
    app,
    start,
    handler
}