var path = require('path')
var pkg = require('../package.json')
var vendors = Object.keys(pkg.dependencies)

module.exports = {
  entry: {
    app: './src/main.js',
    vendors: vendors
  },
  output: {
    path: path.resolve(__dirname, '../dist/static'),
    publicPath: '/static/',
    filename: '[name].js'
  },
  externals:[
    require('webpack-require-http')
  ],
  resolve: {
    extensions: ['', '.js', '.vue','.css'],
    root: path.join(__dirname, 'node_modules'),
    alias: {
      'src': path.resolve(__dirname, '../src'),
      'jquery': path.resolve(__dirname, '../node_modules/jquery/dist/jquery.min'),
      'jquery.slimscrooll': path.resolve(__dirname, '../src/assets/js/jquery.slimscroll'),
      'jquery.blockUI': path.resolve(__dirname, '../src/assets/js/jquery.blockUI'),
      'jquery.scrollTo': path.resolve(__dirname, '../src/assets/js/jquery.scrollTo.min'),
      'dataTables.bootstrap': path.resolve(__dirname, '../node_modules/datatables.net-bs/js/dataTables.bootstrap'),
      'select2': path.resolve(__dirname, '../node_modules/select2/dist/js/select2.min.js'),
      'select2.lang': path.resolve(__dirname, '../node_modules/select2/dist/js/i18n/zh-CN.js'),
      'ht': path.resolve(__dirname, '../src/assets/js/ht.js'),
      'jquery.setBackground':path.resolve(__dirname, '../src/assets/js/jquery.setBackground'),
      'html2canvas':path.resolve(__dirname, '../src/assets/js/html2canvas.js'),
      'jsPDF':path.resolve(__dirname, '../src/assets/js/jspdf.debug.js'),
      'filesaver':path.resolve(__dirname, '../src/assets/js/filesaver.js'),
      'jquery.wordexport':path.resolve(__dirname, '../src/assets/js/jquery.wordexport.js'),
      'sortable':path.resolve(__dirname, '../src/assets/js/sortable.js'),
    },
  externals: {
    'jquery': 'jQuery',
  },
  },
  resolveLoader: {
    root: path.join(__dirname, 'node_modules')
  },
  module: {
    /*
    preLoaders: [
      {
        test: /\.vue$/,
        loader: 'eslint',
        exclude: /node_modules/
      },
      {
        test: /\.js$/,
        loader: 'eslint',
        exclude: [/node_modules/, /jquery.app/]
      }
    ],
     */
    loaders: [
      {
        test: /\.vue$/,
        loader: 'vue'
      },
      {
        test: /\.js$/,
        loader: 'babel',
        exclude: /node_modules/
      },
      {
        test: /\.json$/,
        loader: 'json'
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'url',
        query: {
          limit: 10000,
          name: '[name].[ext]?[hash:7]'
        }
      },
      {
        test: /\.(woff|woff2)$/,
        loader: "url-loader?limit=10000&mimetype=application/font-woff"
      },
      {
        test: /\.ttf$/,
        loader: "file-loader"
      },
      {
        test: /\.eot$/,
        loader: "file-loader"
      }
    ]

  },
  eslint: {
    formatter: require('eslint-friendly-formatter')
  },
  stats: { children: false }
}
