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
			<b-col v-for="(item, index) in items" class="asset m-4 siz" v-bind:id="item.serialNumberInserv">

				<b-row align-v="start">

					<b-col class="text-left pl-1" cols="1">
						<font-awesome-icon v-on:click="saveFile(index)" download v-b-tooltip.hover title="Download JSON" :icon="['fas', 'file-download']" class="hover_mouse"/>
					</b-col>

					<b-col class="text-center">
						<b>Asset {{index+1}}</b>
					</b-col>

					<b-col class="text-left pl-1 mr-1" cols="1">
						<font-awesome-icon :icon="['far', 'hdd']" class="hover_mouse" v-bind:id="'popover_' + item.serialNumberInserv" v-b-tooltip.hover title="History"/>
					</b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Serial Number:</u> {{ item.serialNumberInserv }}</b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Tenants:</u>
						<font v-for="(tenant, i) in item.authorized.tenants">
							<span v-if="tenant.length-2 === i || tenant.length-1 === i || tenant.length === i">
								{{tenant}}
							</span>
							<span v-else>
								{{tenant}},
							</span>
						</font>
					</b-col>
				</b-row>

				<b-row>
					<b-col class=""><u>Last Updated:</u> {{ item.updated }}</b-col>
				</b-row>

				<b-row>
					<b-col class="text-center mb-1">
						<b-button v-b-modal="'myModal'" @click="sendInfo(item, index)">
							View more information
						</b-button>
					</b-col>
				</b-row>

				<b-popover v-bind:target="'popover_' + item.serialNumberInserv" triggers="click" placement="auto" title="History">
					History shown here
				</b-popover>

			</b-col>
		</b-row>
		<b-row align-v="end" class="mt-4 mb-4">
			<b-col class="text-center">© 2018 Copyright: FileBrowser developed for HPE by University of Massachusetts</b-col>
		</b-row>

		<b-modal id="myModal" hide-footer v-bind:title="'Asset ' + (machine_index+1)">
			<b-container fluid>
				<b-tabs>

				<b-tab title="General" active>
					<br><tree-view :data="general_json(machine)"></tree-view>
				</b-tab>

				  <b-tab title="System">
				  	<br><tree-view :data="machine.system"></tree-view>
				  </b-tab>

				  <b-tab title="Capacity">
				    <br><tree-view :data="machine.capacity"></tree-view>
				  </b-tab>

				  <b-tab title="Performance">
				    <br><tree-view :data="machine.performance"></tree-view>
				  </b-tab>

				  <b-tab title="Disks">
				    <br><tree-view :data="machine.disks"></tree-view>
				  </b-tab>

				  <b-tab title="Nodes">
				    <br><tree-view :data="machine.nodes"></tree-view>
				  </b-tab>

				  <b-tab title="Authorized">
				  	<br><tree-view :data="machine.authorized"></tree-view>
				  </b-tab>

				</b-tabs>
			</b-container>
		</b-modal>

	</b-container>
</div>
</template>

<script>

export default {
  name: 'Assets',
  filters: {
  	pretty: function(value) {
      return JSON.stringify(value, null, 2);
    }
  },
  data() {
  	return {
	  	items: [],
	  	machine: '',
	  	machine_index: 0
	}
  },
  created: function() {
  	if (!this.$session.exists()) {
  		this.$router.push('/')
  	}
  	else {
  		var username = this.$session.getAll().username
  		var password = this.$session.getAll().password
  		const path = 'http://aws.kylesilverman.com:5000/machines?'
  		//const path = 'http://localhost:5000/machines?'
		
  		const data = "username="+username+"&password="+password
  		this.$http.post(path+data).then(response => {
  			console.log(response.body)
 			var body = response.body
  			/*for(var i=0; i < body.length; i++)
  			{
  				var date = new Date(body[i].last_update.$date);
  				var new_date = date.toISOString();
  				body[i].last_update.$date = new_date.substring(0, new_date.length-5)+"Z"
  			}*/
  			this.items = body;
  		}).catch(error => {
  			console.log(this.$session.getAll())
  		})
  	}
  },
  methods: {
  	sendInfo(machine, machine_index) {
        this.machine = machine;
        this.machine_index = machine_index;
    },
    general_json(item) {
    	return {"serialNumberInserv": item.serialNumberInserv, "updated": item.updated, "date": item.date}
    },
  	onLogout () {
  		this.$session.destroy()
  		this.$router.push('/')
  	},
  	saveFile: function(index) {
  		var item_object = this.items[index];
        const data = JSON.stringify(item_object, null, 2);//JSON.stringify(item_object)
        const file_name = item_object.serialNumberInserv+"-"+item_object.updated
        return this.downloadFile(data, this.strip_time(file_name))
  	},
  	downloadFile(response, filename) {
	  // It is necessary to create a new blob object with mime-type explicitly set
	  // otherwise only Chrome works like it should
	  var newBlob = new Blob([response], {type: 'application/json'})

	  // IE doesn't allow using a blob object directly as link href
	  // instead it is necessary to use msSaveOrOpenBlob
	  if (window.navigator && window.navigator.msSaveOrOpenBlob) 
	  {
	    window.navigator.msSaveOrOpenBlob(newBlob)
	    return
	  }

	  // For other browsers:
	  // Create a link pointing to the ObjectURL containing the blob.
	  const data = window.URL.createObjectURL(newBlob)
	  var link = document.createElement('a')
	  link.href = data
	  link.download = filename + '.json'
	  link.click()
	  setTimeout(function () 
	  {
	    // For Firefox it is necessary to delay revoking the ObjectURL
	    window.URL.revokeObjectURL(data)
	  }, 100)
	},
	strip_time(str) {
		for(var i=0; i < str.length; i++)
		{
			if(str[i] == "T")
			{
				return str.substring(0, i);
			}
		}
	}
  } 
}
</script>

<style src="../assets/css/filebrowser.css"></style>
