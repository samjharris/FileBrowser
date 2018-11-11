<template>
	<p>You should not see this</p>
</template>

<script>
import router from '../router'

export default {
  name: 'Error404',
  created: function() {
  		router.push({ name: 'Login'});
  }
}
</script>