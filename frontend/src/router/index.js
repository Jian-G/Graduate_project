import Vue from 'vue'
import Router from 'vue-router'
import Log from "@/components/Log"
import Transmit from "@/components/Transmit"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path:"/Transmit",
      component: Transmit
    },
    {
      path: '/Logs',
      name: 'log',
      component: Log
    }
  ]
})
