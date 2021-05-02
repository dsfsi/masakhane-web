  
const path = require('path')

module.exports = {
  entry: path.resolve(__dirname, 'src', 'index.js'),
  output: {
    path: path.resolve(__dirname, 'public'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  devServer: {
    contentBase: path.resolve(__dirname, 'public'),
    open: true,
    clientLogLevel: 'silent',
    port: 8000,
    historyApiFallback: true,
    compress: true,
    public: 'masakhane.translate.io'
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /node_modules/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                "targets": "defaults" 
              }],
              '@babel/preset-react'
            ]
          }
        }]
      },
      {
        test: /\.(jpg|png|svg)$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /node_modules/,
        loader: 'url-loader',
        options: {
        limit: 25000,
        performance: {
          hints: false,
          maxEntrypointSize: 512000,
          maxAssetSize: 512000
      }
      },
      
    }
    
    ]
  }
}
