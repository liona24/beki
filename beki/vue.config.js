const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, "../dist/bundle/static"),
  devServer: {
    proxy: {
      '^/(images|api)/*': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        logLevel: 'debug'
      }
    }
  }
}
