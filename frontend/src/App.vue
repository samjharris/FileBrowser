<template>

  <!-- Root component to mount to -->

  <div id="app"><router-view/></div>

</template>



<script>

  import 'bootstrap/dist/css/bootstrap.css'

  import 'bootstrap-vue/dist/bootstrap-vue.css'


  export default {

    name: 'app'

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
