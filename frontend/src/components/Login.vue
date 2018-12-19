<template>

  <div class="login">

    <b-alert variant="danger" dismissible
      
      :show="error" @dismissed="error=false">

      Invalid username or password

    </b-alert>


    <b-form class="login" @submit.prevent="onSubmit">
      
      <!-- Username Field -->

      <b-form-group id="usernamegroup" class="igroup"

        label="Username" label-for="username">

        <b-form-input id="username" class="input"

          type="text" v-model="form.username" required>

        </b-form-input>
      
      </b-form-group>


      <!-- Password Field -->

      <b-form-group id="passwordgroup" class="igroup"

        label="Password" label-for="password">
        
        <b-form-input id="password" class="input"

          type="password" v-model="form.password" required>
            
        </b-form-input>

      </b-form-group>


      <!-- Submit button -->

      <b-button type="submit" class="button">Submit</b-button>

    </b-form>

  </div>

</template>



<script>

  // 3rd party tool to build query strings

  import queryString from 'query-string';


  export default {

    name: 'Login',

    data() {

      return {

        error: false,
      
        form: {
      
          username: '',
      
          password: ''
      
        }
      
      }

    },

    created: function() {
      if (this.$session.exists()) {
        this.$session.destroy()
      } 
    },

    methods: {

      onSubmit(event) {

        const base = 'http://aws.kylesilverman.com:5000/login';
        //const base = 'http://localhost:5000/login';

        const endpoint = base + '?' + queryString.stringify(this.form);


        this.$http.post(endpoint)

          .then(resp => {
            
            this.$session.start();

            this.$session.set('username', this.form.username);
            
            this.$session.set('password', this.form.password);

            this.$session.set('page', 1);
            
            this.$router.push({ name: 'Assets' });

          })

          .catch(err => { this.error = true; });
    
      }
    
    }

  }

</script>