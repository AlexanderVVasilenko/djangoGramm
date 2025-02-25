const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    entry: path.resolve(__dirname, 'static/js/index.js'),
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: "bundle.js",
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|jpg|jpeg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            outputPath: "images"
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new BundleTracker({
            path: path.resolve(__dirname),
            filename: 'webpack-stats.json'})
    ],
    mode: 'development'
}