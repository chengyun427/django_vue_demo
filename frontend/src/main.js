// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

//ElementUI配置
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

//配置axios
import axios from 'axios'

//配置vuex
import store from './store/store'

//时间格式化
import moment from 'moment'

import "babel-polyfill";
import 'url-search-params-polyfill';//解决axios使用的URLSearchParms，在ie下未定义的错误
import httpService from './service/http-service';//封装axios接口强求

//引入阿里巴巴图标
import './assets/ali_icon/iconfont.css'


Vue.use(ElementUI);
Vue.prototype.$axios = httpService;
Vue.prototype.$moment = moment;//时间格式化


Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  store,
  components: { App },
  template: '<App/>'
});
