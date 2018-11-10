<template>
  <div id="app">
    <Assets/>
    <Login place="America"/>
  </div>
</template>

<script>
import Assets from './components/Assets.vue'
import Login from './components/Login.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
  name: 'app',
  components: {
    Assets, Login
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100% !important;
}
</style>
