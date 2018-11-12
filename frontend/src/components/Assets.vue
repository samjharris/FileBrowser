<template>
<div>
	<b-navbar variant="dark" type="dark">
		<b-navbar-brand tag="h1" class="mb-0">JSON Derulo</b-navbar-brand>
		<b-navbar-brand tag="h3" class="mb-0"> 
			<b-form @submit="onLogout">
				<b-button type="submit">Logout</b-button>
			</b-form>
		</b-navbar-brand>
	</b-navbar>

	<b-container fluid class="h-100">
		<b-row align-h="start">
			<b-col v-for="(item, index) in items" class="asset m-4 siz">

				<b-row align-v="start">
					<b-col class="text-left pl-1" cols="1"><font-awesome-icon v-b-tooltip.hover title="Download JSON" :icon="['fas', 'file-download']" /></b-col>
					<b-col class="text-center"><b>Asset {{index+1}}</b></b-col>
					<b-col class="text-left pl-1 mr-1" cols="1"><font-awesome-icon :icon="['far', 'hdd']" /></b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Serial Number:</u> {{ item.serial }}</b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Tenants:</u>
						<font v-for="(tenant, i) in item.tenants">
							<span v-if="tenant.length-2 === i">
								{{ tenant }}
							</span>
							<span v-else>
								{{ tenant }},
							</span>
						</font>
					</b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Last Updated:</u> {{ item.last_updated }}</b-col>
				</b-row>

				<b-row>
					<b-col class="text-center">
						<b-link v-b-modal="'modal_' + index">
							View more information
						</b-link>
					</b-col>
				</b-row>

				<b-modal :id="'modal_' + index" v-bind:title="'Asset ' + (index+1)" hide-footer>
					<b-container fluid>
						<b-tabs>

						  <b-tab title="System" active>
						  	<br>
						  	<b-row cols="2">
							    <b-col class="outline">
							    	Serial Number: {{ item.serial }}
							    </b-col>
							    <!--
							    <b-col class="outline text-center">
							    	Port Info
							    	<br>
							    	<b-card no-body>
								    	<b-tabs card vertical>
								    		<template v-for="j in 9">
									    		<b-tab :title="j" v-if="j == 1" active><br>Tab: {{ j }}</b-tab>
									    		<b-tab :title="j" v-else><br>Tab: {{ j }}</b-tab>
								    		</template>
								    	</b-tabs>
							    	</b-card>
							    </b-col>
								-->
							</b-row>
						  </b-tab>

						  <b-tab title="Capacity" >
						    <br>Capacity
						  </b-tab>

						  <b-tab title="Performance">
						    <br>Performance
						  </b-tab>

						  <b-tab title="Disks">
						    <br>Disks
						  </b-tab>

						  <b-tab title="Nodes">
						    <br>Nodes
						  </b-tab>

						  <b-tab title="Authorized">
						    <br>Authorized
						  </b-tab>

						</b-tabs>
					</b-container>
				</b-modal>

			</b-col>
		</b-row>
		<b-row align-v="end" class="mt-4 mb-4">
			<b-col class="text-center">© 2018 Copyright: FileBrowser developed for HP by University of Massachusetts</b-col>
		</b-row>
	</b-container>
</div>
</template>

<script>
export default {
  name: 'Assets',
  data() {
  	return {
	  	items: [
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '22156', tenants: ['Kyle', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '12345', tenants: ['John', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '54321', tenants: ['Adam', 'hpe'], last_updated: '18/04/13 05:27:55' },
	      { serial: '83027', tenants: ['Dan', 'hpe'], last_updated: '18/04/13 05:27:55' }
	    ]
	}
  },
  beforeCreate: function() {
  	if (!this.$session.exists()) {
  		this.$router.push('/')
  	}
  	else {
  		const path = 'http://aws.kylesilverman.com:5000/machines'
  		this.$http.post(path).then(response => {
  			console.log(response.text)
  		}).catch(error => {
  			console.log(this.$session.getAll())
  		})
  	}
  },
  methods: {
  	onLogout () {
  		this.$session.destroy()
  		this.$router.push('/')
  	}
  } 
}
</script>

<style src="../assets/css/filebrowser.css"></style>