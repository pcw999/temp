const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.plugins.delete('prefetch');
  },
  configureWebpack: {
    target: 'electron-renderer'
  },
  devServer: {
    port: 8080,
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:5000',
        ws: true,
        changeOrigin: true
      }
    }
  }
})
