import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Assets from '@/components/Assets'
import Login from '@/components/Login'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/machines',
      name: 'Assets',
      component: Assets
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
