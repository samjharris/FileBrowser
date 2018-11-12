<template>
	<b-container>
		<b-row class="down">
			<b-col>
				<b-form @submit="onSubmit">
					<b-form-group id="label_username" label="Username:" label-for="username">
						<b-form-input id="username" type="text" v-model="form.username" required placeholder="Enter username"></b-form-input>
					</b-form-group>

					<b-form-group id="label_password" label="Password:" label-for="password">
						<b-form-input id="password" type="password" v-model="form.password" required placeholder="Enter password"></b-form-input>
					</b-form-group>

					<b-button type="submit" variant="primary">Submit</b-button>
				</b-form>
			</b-col>
		</b-row>
	</b-container>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault();
      
      const path = 'http://localhost:5000/login?'
      const data = "tenant="+this.form.username+"&password="+this.form.password
      this.$http.post(path+data).then(response => {
      this.$session.start()
      this.$session.set('tenant', this.form.username)
      this.$session.set('password', this.form.password)
      this.$router.push({
          name: 'Assets',
        })
      }).catch(error => {
      	console.log("username: "+this.form.username+" password: "+this.form.password)
      	console.log(error)
    })
    }
  }
  /*
  props: {
    place: String
  }*/
}
</script>