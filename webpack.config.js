const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
    mode: 'development',
    context: __dirname,
    entry: './static/js/app',
    output: {
        path: path.resolve('./static/bundles/'),
        publicPath: '/static/bundles/',
        filename: 'app.js'
    },

    plugins: [
        new BundleTracker({ 
            path: __dirname, 
            filename: "webpack-stats.json" 
        }),
        new VueLoaderPlugin(),
    ],

    module: {
        rules:  [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: 'css-loader'
            }
        ],
    },
    resolve: {
        alias: {vue: 'vue/dist/vue.cjs.js'}
    },

};
