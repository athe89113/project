import Vue from 'vue'
import VueValidator from 'vue-validator'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import VueDND from 'awe-dnd'
import RegisterRouters from './lib/routers'
import Highlight from './lib/Highlight'
import Api from './lib/api'
import progress from 'vue-progressbar'
import YSUI from './components/index'
import 'babel-polyfill';

var VueClipboard = require('vue-clipboard');

global.$ = global.jQuery = require('jquery')
window.collect = require('collect.js');
require('bootstrap-webpack')
require('./assets/css/core.css')
require('./assets/css/components.css')
require('./assets/css/icons.css')
require('./assets/css/dashboard.css')
require('./assets/css/public.css')
require('./assets/css/ys.css')

import App from './app'

Vue.use(progress)
Vue.use(VueValidator)
Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(Highlight)
Vue.use(VueClipboard)
Vue.use(YSUI)
Vue.use(VueDND)

try {
  Vue.http.options.root = require('../.config').backendServer
} catch(err) {
  Vue.http.options.root = ''
}

global.Vue = Vue
var router = new VueRouter({
  hashbang: false,
  history: true,
  saveScrollPosition: true,
  transitionOnLoad: true
})
document.title = '安全管理平台';
router.beforeEach(function(transition){
  if(transition.to.path==='/login'){
    return true;
  }
  Vue.prototype.$progress.start(3000)
  Api.user.checkLogon(transition)
  if(transition.to.name=="workorder-apply" && localStorage.getItem('role_type')==1){
    return false;
  }
  if(transition.to.name=="workorder-deal" && localStorage.getItem('role_type')==3){
    return false;
  }
})

router.afterEach(function(transition){
  Vue.prototype.$progress.finish()
  //console.log(transition.to.menu)
})

RegisterRouters(router)

router.start(App, '#app')



