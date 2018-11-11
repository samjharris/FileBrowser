<template>
<<<<<<< HEAD
	
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
=======
	<h1>this is a test</h1>
>>>>>>> 500cdad8f7cc9c8d850dcfc7a4e8f1a4283b7fc2
	
</template>

<script>
export default {
<<<<<<< HEAD
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
      //alert(JSON.stringify(this.form));
      const path = 'https://cors-anywhere.herokuapp.com/http://aws.kylesilverman.com/login?'
      const data = "tenant="+this.form.username+"&password="+this.form.password
      this.$http.post(path+data).then(response => {
      	window.location = window.location+"assets"
      }).catch(error => {
      	console.log("username: "+this.form.username+" password: "+this.form.password)
      	console.log(error)
    })
    }
  }
=======
  name: 'Login'
>>>>>>> 500cdad8f7cc9c8d850dcfc7a4e8f1a4283b7fc2
  /*
  props: {
    place: String
  }*/
}
</script>