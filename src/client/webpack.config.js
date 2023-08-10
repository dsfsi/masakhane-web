const path = require("path");

module.exports = {
  entry: path.resolve(__dirname, "src", "index.js"),
  output: {
    path: path.resolve(__dirname, "public"),
    filename: "bundle.js",
    publicPath: "/",
  },
  devServer: {
    contentBase: path.resolve(__dirname, "public"),
    open: true,
    clientLogLevel: "silent",
    host: "0.0.0.0",
    port: 3000,
    historyApiFallback: true,
    compress: true,
    public: "translate.masakhane.io:80",
    // proxy: {
    //   '/': {
    //       target: 'http://localhost:5000',
    //       pathRewrite: { '^/api': '' },
    //   },
    //   "changeOrigin":true
    // }
    proxy: {
      "/": {
        target: "http://[::1]:5000",
        // todo: make the ip a configuration environment variable
        // target: 'http://45.147.99.147:5000',
        changeOrigin: true,
        // target: "http://127.0.0.1:5000",
        bypass: function (req, res, proxyOptions) {
          if (req.headers.accept.indexOf("html") !== -1) {
            console.log("Skipping proxy for browser request.");
            return "/index.html";
          }
        },
      },
    },
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, "src"),
        exclude: /node_modules/,
        use: [
          {
            loader: "babel-loader",
            options: {
              presets: [
                [
                  "@babel/preset-env",
                  {
                    targets: "defaults",
                  },
                ],
                "@babel/preset-react",
              ],
            },
          },
        ],
      },
      {
        test: /\.(jpg|png|svg)$/,
        include: path.resolve(__dirname, "src"),
        exclude: /node_modules/,
        loader: "url-loader",
        options: {
          limit: 25000,
          performance: {
            hints: false,
            maxEntrypointSize: 512000,
            maxAssetSize: 512000,
          },
        },
      },
    ],
  },
};
