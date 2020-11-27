module.exports = {
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
