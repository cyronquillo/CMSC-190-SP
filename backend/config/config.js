'use strict'

const path = require('path');

module.exports = {
    APP_NAME: 'Transcript Verifier',
    APP_URL: 'http://localhost:5000',


    PORT: 5000,
    STATIC_PORT: 5000,
    IP: '127.0.0.1',


    ASSETS_DIR: path.normalize(__dirname + '/../front-end')

}