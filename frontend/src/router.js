import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login'
import Assets from './components/Assets'
import error404 from './components/error404'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/assets',
      name: 'Assets',
      component: Assets
    },
    {
      path: '*',
      redirect: "/"
      //name:'Error404',
      //component: error404
    }
  ]
})
