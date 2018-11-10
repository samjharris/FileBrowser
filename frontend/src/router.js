import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from './components/HelloWorld'
import Assets from './components/Assets'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Assets',
      component: Assets
    },
    {
      path: '/assets',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
