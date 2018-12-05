<template>
<div>
	<b-navbar variant="dark" type="dark">
		<b-navbar-brand tag="h1" class="mb-0">FileBrowser</b-navbar-brand>
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
								<b>{{item.system.companyName}}</b>	
					</b-col>


					<span v-if="parseFltFreeCapacity(item.capacity.total.freePct) <= 30">
						<b-col class="text-left pl-1" cols="1">
								<font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="red_icon_hover" v-b-tooltip.hover title="Warning: Capacity Low"/>
				        </b-col>
					</span>


					<b-col class="text-left pl-1 mr-1" cols="1">
						<font-awesome-icon :icon="['far', 'hdd']" class="hover_mouse" v-bind:id="'popover_' + item.serialNumberInserv" v-b-tooltip.hover title="History"/>
					</b-col>
				</b-row>

				<b-row>
					<b-col class=""><b>Serial Number:</b> {{ item.serialNumberInserv }}</b-col>
				</b-row>

				<b-row>
					<b-col class=""><b>Tenants:</b>
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
					<b-col class=""><b>Last Updated:</b> {{ item.updated }}</b-col>
				</b-row>


				<b-row>
					<b-col class="">
						<b>Capacity Available:</b> {{ parseFltFreeCapacity(item.capacity.total.freePct) +"%"  }}
					</b-col>
				</b-row>

				<b-row>
					<b-col class = "">
						<b-progress class="mt-1" :max="max" show-value>
							<b-progress-bar :value="parseFloat(parseFltFreeCapacity(item.capacity.total.freePct))" variant="success"></b-progress-bar>
      						<b-progress-bar :value="100-parseFloat(parseFltFreeCapacity(item.capacity.total.freePct))" variant="danger"></b-progress-bar>
    					</b-progress>
    				</b-col>
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

			<b-col class="text-center">
					<h3>{{ this.emptyBodyText }}</h3>			
			</b-col>

	</b-container>

	<b-navbar variant="dark" type="dark">		
			<b-navbar-brand tag="h1" class="mb-0"></b-navbar-brand>
			
			<b-pagination size="lg" :total-rows="numSystems" v-model="currentPage" :per-page="20" hide-ellipsis hide-goto-end-buttons>
    		</b-pagination>

  			<b-navbar-brand tag="h1" class="mb-0"></b-navbar-brand>
	</b-navbar>
		
	<b-row align-v="end" class="mt-4 mb-4">
			<b-col class="text-center">© 2018 Copyright: FileBrowser developed for HPE by JSON_Derulo, University of Massachusetts</b-col>
	</b-row>
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
	  	machine_index: 0,
	  	currentPage: 1,
	  	lastPage:1,
	  	emptyBodyText:"",
	  	numSystems:Number.MAX_VALUE //don't change this, this is spegetti code
	}
  },
  created: function() {
  	if (!this.$session.exists()) {
  		this.$router.push('/')
  	}
  	else {
  		var username = this.$session.getAll().username
  		var password = this.$session.getAll().password
  		var page = this.$session.getAll().page
  		this.currentPage = parseInt(page)
  		//const path = 'http://aws.kylesilverman.com:5000/machines?'
  		const path = 'http://localhost:5000/machines?'
  		const data = "username="+username+"&password="+password+"&page="+page

  		console.log("Page from session: " + page);
  		console.log("CurrentPage for v-model: " + this.currentPage)
  		
  		this.$http.post(path+data).then(response => {
  			console.log(response.body)
 			var body = response.body
 			this.numSystems = body.numSystems;
  			this.items = body.machines;
  		}).catch(error => {
  			console.log(this.$session.getAll())
  		})
  	}
  },
  updated: function() {
  	if(this.currentPage != this.lastPage){
  		this.lastPage = this.currentPage
  		if (!this.$session.exists()) {
  			this.$router.push('/')
  		}
  		else {
  			var username = this.$session.getAll().username
  			var password = this.$session.getAll().password

  			//const path = 'http://aws.kylesilverman.com:5000/machines?'
  			const path = 'http://localhost:5000/machines?'
  			const data = "username="+username+"&password="+password+"&page="+this.currentPage
  			this.$session.set('page', this.currentPage);
  			this.$http.post(path+data).then(response => {
  				console.log(response.body)
 				var body = response.body
 				this.numSystems = body.numSystems;
  				this.items = body.machines;
  				if(body.length === 0){
  					this.emptyBodyText = "There are no more systems to display. Please navigate to a previous page."
  				}else{
  					this.emptyBodyText = ""
  				}
  			}).catch(error => {
  				console.log(this.$session.getAll())
  			})
  		}
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
  	getVariantType: function(availableCapacity) {
        if (availableCapacity <= 30) {
						console.log("Danger")
            return "danger"
        }
        else {
            return "success"
        }
    },
    parseIntFreeCapacity: function(freePct){
	     return Math.round(freePct);
	},
	parseFltFreeCapacity: function(freePct){
	     return freePct.toFixed(2); 
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
