var express = require('express')
var webpack = require('webpack')
var config = require('./webpack.dev.conf')

var app = express()
var compiler = webpack(config)

// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')())

// serve webpack bundle output
app.use(require('webpack-dev-middleware')(compiler, {
  publicPath: config.output.publicPath,
  stats: {
    colors: true,
    chunks: false
  }
}))

// enable hot-reload and state-preserving
// compilation error display
app.use(require('webpack-hot-middleware')(compiler))

// 支持api代理解决跨域问题
app.use(express.static('public'));

var httpProxy = require('http-proxy');
var apiProxy = httpProxy.createProxyServer();
var apiServer = ''
try {
  apiServer = require('../.config').apiServer
} catch(err) {
  apiServer = 'http://127.0.0.1:8080/'
}
var apiServerHost = /http:\/\/=?(\S*)(?=\/)/.exec(apiServer)[1]

app.all('/api/*', function(req, res){
  apiProxy.web(req, res, {target: apiServer}, function(e) {
      console.log('Proxy server error: "' + e + '"')
    })
})
app.all('/media/*', function(req, res){
  apiProxy.web(req, res, {target: apiServer}, function(e) {
    console.log('Proxy server error: "' + e + '"')
  })
})

apiProxy.on('proxyReq', function (proxyReq, req, res) {
  proxyReq.setHeader('Host', apiServerHost);
});

app.listen(10080, 'localhost', function (err) {
  if (err) {
    console.log(err)
    return
  }
  console.log('Listening at http://localhost:10080')
})
