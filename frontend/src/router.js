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
<<<<<<< HEAD
      redirect: "/"
      //name:'Error404',
      //component: error404
=======
      name:'Error404',
      component: error404
>>>>>>> 500cdad8f7cc9c8d850dcfc7a4e8f1a4283b7fc2
    }
  ]
})
