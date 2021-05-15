// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import ElementUI from 'element-ui'
import echarts from "echarts"
import VideoPlayer from 'vue-video-player'

Vue.prototype.$echarts = echarts;
import '../src/assets/style.css'
import './theme/index.css'

Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.use(VueRouter)
axios.defaults.baseURL = 'http://127.0.0.1:5000';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
Vue.use(VueAxios, axios)
Vue.use(VideoPlayer)

const router = new VueRouter({
    routes: [
        {path: "/App", component: App, meta: {title: "vue_flask"},},
    ],
    mode: "history"
})

// // 全局注册组件
Vue.component("App", App);

/* eslint-disable no-new */
new Vue({
      el: '#app',
      router,
      render: h => h(App),
    })
