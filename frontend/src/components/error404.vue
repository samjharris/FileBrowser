<template>
</template>

<script>
import router from '../router'

export default {
  name: 'Login',
  created: function() {
  		router.push({ name: 'Login'});
  }
}
</script>