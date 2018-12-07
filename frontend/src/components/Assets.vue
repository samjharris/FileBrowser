<template>
<div>

	<!------------------>
	<!-- BEGIN HEADER -->
	<!------------------>
	<b-navbar toggleable="md" type="dark" variant="dark">
  		<b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
  		
  		<!-- TITLE -->
  		<b-navbar-brand href="#">FileBrowser</b-navbar-brand>
  		<b-collapse is-nav id="nav_collapse">
			<b-navbar-nav class="ml-auto">
				
				<!-- SORT ORDER DROPDOWN -->
    			<b-dropdown variant="link" size="lg" no-caret>
    				<template slot="button-content"><font-awesome-icon :icon="this.sortByIcon"/>
    					<span class="sr-only">Filter</span>
    				</template>
    					<b-dropdown-item v-on:click="setSort('fslh')">Free space: Low to High</b-dropdown-item>
    					<b-dropdown-item v-on:click="setSort('fshl')">Free space: High to Low</b-dropdown-item>
    					<b-dropdown-item v-on:click="setSort('snlh')">Serial number: Low to High</b-dropdown-item>
    					<b-dropdown-item v-on:click="setSort('snhl')">Serial number: High to Low</b-dropdown-item>
    					<b-dropdown-item v-on:click="setSort('cnaz')">Company name: A to Z</b-dropdown-item>
    					<b-dropdown-item v-on:click="setSort('cnza')">Company name: Z to A</b-dropdown-item>
  				</b-dropdown>

  				<!-- SEARCH FORM/BUTTON -->
      			<b-nav-form>
        			<b-form-input size="md" class="mr-md-2" type="text" v-model="searchForm" placeholder="serial # or company name"/></b-form-input>
        			<b-button size="md" class="my-2 my-md-0" type="button" v-on:click="onSearch">Search</b-button>
      			</b-nav-form>

      	        <!-- LOGOUT BUTTON -->
      			<b-navbar-brand tag="h3" class="mb-0 px-2"> 
					<b-form @submit="onLogout">
						<b-button type="submit">Logout</b-button>
					</b-form>
				</b-navbar-brand>

      		</b-navbar-nav>
  		</b-collapse>
	</b-navbar>

	<!----------------------->
	<!-- BEGIN SEARCH TEXT -->
	<!----------------------->
	<b-row v-show="this.isSearch && !showSpinner">
		<b-col class="text-center">
				<br>
				<h3>Showing results for &quot;{{ this.searchInput }}&quot; &nbsp; 
					<font-awesome-icon v-on:click="clearSearch" v-b-tooltip.hover title="Clear search" :icon="['fas', 'times-circle']" class="hover_mouse"/> 
				</h3>	
						
		</b-col>
	</b-row>	

	<!--------------------------->
	<!-- BEGIN ASSET CONTAINER -->
	<!--------------------------->
	<b-container fluid class="asset-parent h-100">
		<!-- ASSET GRID -->
		<b-row align-h="start" v-show="!showSpinner">
			<b-col v-for="(item, index) in items" class="asset m-4 siz" v-bind:id="item.serialNumberInserv">

				<!-- ICONS/TITLE -->
				<b-row class="info" align-v="start">

					<!-- DOWNLOAD ICON -->
					<b-col class="text-left pl-1" cols="1">
						<font-awesome-icon v-on:click="saveFile(index)" download v-b-tooltip.hover title="Download JSON" :icon="['fas', 'file-download']" class="hover_mouse"/>
					</b-col>

					<!-- ASSET TITLE -->
					<b-col class="text-center">
						<b>{{item.system.companyName}}</b>	
					</b-col>

					<!-- CAPACITY WARNING -->
					<span v-if="parseFltFreeCapacity(item.capacity.total.freePct) <= 30">
						<b-col class="text-left pl-1" cols="1">
							<font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="red_icon_hover" v-b-tooltip.hover title="Warning: Capacity Low"/>
				        </b-col>
					</span>

					<!-- HISTORY ICON -->
					<b-col class="text-left pl-1 mr-1" cols="1">
						<font-awesome-icon :icon="['far', 'hdd']" class="hover_mouse" v-bind:id="'popover_' + item.serialNumberInserv" v-b-tooltip.hover title="History"/>
					</b-col>

				</b-row>

				<!-- SERIAL NUMBER -->
				<b-row>
					<b-col class=""><b>Serial Number:</b> {{ item.serialNumberInserv }}</b-col>
				</b-row>

				<!-- TENANT LIST -->
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

				<!-- LAST UPDATE -->
				<b-row>
					<b-col class="">
						<b>Last Updated:</b> {{ item.updated }}
					</b-col>
				</b-row>

				<!-- CAPACITY AVAILABLE -->
				<b-row>
					<b-col class="">
						<b>Capacity Available:</b> {{ parseFltFreeCapacity(item.capacity.total.freePct) +"%"  }}
					</b-col>
				</b-row>

				<!-- CAPACITY GRAPH -->
				<b-row>
					<b-col class = "">
						<b-progress class="mt-1" show-value>
							<b-progress-bar :value="parseFloat(parseFltFreeCapacity(item.capacity.total.freePct))" variant="success"></b-progress-bar>
      						<b-progress-bar :value="100-parseFloat(parseFltFreeCapacity(item.capacity.total.freePct))" variant="danger"></b-progress-bar>
    					</b-progress>
    				</b-col>
				</b-row>
				
				<!-- MORE INFORMATION BUTTON -->
				<b-row>
					<b-col class="text-center mb-1 mt-1">
						<b-button v-b-modal="'myModal'" @click="sendInfo(item, index)">
							View more information
						</b-button>
					</b-col>
				</b-row>

				<!-- HISTORY POPOVER -->
				<b-popover v-bind:target="'popover_' + item.serialNumberInserv" triggers="click" placement="auto" @show="onHistoryShow(item.serialNumberInserv)">

					<template slot="title">
						History
				        <b-btn @click="onHistoryClose(item.serialNumberInserv)" class="close" aria-label="Close">
				          <span class="d-inline-block" aria-hidden="true">&times;</span>
				        </b-btn>
				    </template>

				    <b-row v-show="showHistorySpinner">
				    	<b-col>
				    		<div align-self="center" class="history_loader" id="spinner"></div>
				    	</b-col>
				    </b-row>
					<b-row v-for="(hist, history_index) in history_items">
						<b-col>
							<!--<b-alert show variant="dark"> {{ hist.updated }} </b-alert>-->
							<b-button v-if="items[index].date != history_items[history_index].date" variant="outline-secondary" class="mb-1" @click="doHistory(index, history_index, item.serialNumberInserv)">{{ hist.date }}</b-button>
							<span v-if="history_items.length == 1"><b>There is no history for this machine</b></span>	
						</b-col>
					</b-row>
				</b-popover>

			</b-col>
		</b-row>
	
		<!-- MORE INFORMATION MODAL -->
		<b-modal id="myModal" hide-footer v-bind:title="'Asset ' + (machine_index+1)">
			<b-container fluid>
				<b-tabs>
					<b-tab title="General" active>
						<br><tree-view :data="general_json(machine)" :options="{rootObjectKey: 'General'}">></tree-view>
					</b-tab>

				  	<b-tab title="System">
				  		<br><tree-view :data="machine.system" :options="{rootObjectKey: 'System'}">></tree-view>
				  	</b-tab>

				  	<b-tab title="Capacity">
				    	<br><tree-view :data="machine.capacity" :options="{rootObjectKey: 'Capacity'}">></tree-view>
				  	</b-tab>

				  	<b-tab title="Performance">
				    	<br><tree-view :data="machine.performance" :options="{rootObjectKey: 'Performance'}">></tree-view>
				  	</b-tab>

				  	<b-tab title="Disks">
				    	<br><tree-view :data="machine.disks" :options="{rootObjectKey: 'Disks'}">></tree-view>
				  	</b-tab>

				  	<b-tab title="Nodes">
				    	<br><tree-view :data="machine.nodes" :options="{rootObjectKey: 'Nodes'}">></tree-view>
				  	</b-tab>

				  	<b-tab title="Authorized">
				  		<br><tree-view :data="machine.authorized" :options="{rootObjectKey: 'Authorized'}">></tree-view>
				  	</b-tab>
				</b-tabs>
			</b-container>
		</b-modal>

		<!-- SPINNER ROW -->
		<b-row id="row_for_spinner">
			<b-col v-show="showSpinner">
				<br><br><br>
				<div align-self="center" class="loader" id="spinner"></div>
				<br><br><br>
			</b-col>
		</b-row>
	</b-container>

	<!------------------------------>
	<!-- BEGIN PAGINATION NAV BAR -->
	<!------------------------------>
	<b-navbar variant="dark" type="dark" v-show="!showSpinner">	
		<!-- SPACER LEFT -->
		<b-navbar-brand tag="h1" class="mb-0"></b-navbar-brand>
			
			<!-- PAGINATION COMPONENT -->
			<b-pagination size="lg" :total-rows="numSystems" v-model="currentPage" :per-page="20"></b-pagination>

    	<!-- SPACER RIGHT -->
  		<b-navbar-brand tag="h1" class="mb-0"></b-navbar-brand>
	</b-navbar>
		
	<!------------------>
	<!-- BEGIN FOOTER -->
	<!------------------>
	<b-row align-v="end" class="mt-4 mb-4">
		<b-col class="text-center">
			© 2018 Copyright: FileBrowser developed for HPE by JSON_Derulo, University of Massachusetts
		</b-col>
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
	  	history_items: [],
	  	machine: '',
	  	machine_index: 0,
	  	currentPage: 1,
	  	lastPage: 1,
	  	emptyBodyText: "",
	  	numSystems: Number.MAX_VALUE, //don't change this, this is spegetti code
	  	sortByCode: 'fslh',
	  	lastSortByCode: 'fslh',
	  	sortByIcon: ['fas', 'sort-amount-up'],
	  	searchInput: '',
	  	searchForm:'',
	  	isSearch:false,
	  	showSpinner: true,
	  	showHistorySpinner: true,
	  	popoverShow: false
	}
  },


//FOR HISTORY:
//const path = 'http://localhost:5000/history?'
//const data = "username="+username+"&password="+password+"&sni="+serialNumberInserv_to_get_history_for


  created: function() {
  	if (!this.$session.exists()) {
  		this.$router.push('/')
  	}
  	else {
  		var username = this.$session.getAll().username
  		var password = this.$session.getAll().password
  		var page = this.$session.getAll().page
  		var sort = this.$session.getAll().sort
  		this.currentPage = parseInt(page)
  		this.setSort(sort)
  		this.lastSortByCode = sort
  		//const path = 'http://aws.kylesilverman.com:5000/machines?'
  		const path = 'http://localhost:5000/machines?'
  		const data = "username="+username+"&password="+password+"&page="+page+"&sort="+sort
  		
  		
  		this.$http.post(path+data).then(response => {

 			var body = response.body;
 			this.numSystems = body.numSystems;
  			this.items = body.machines;
  			this.showSpinner = false;

  		}).catch(error => {
  			console.log(this.$session.getAll())
  		})
  	}
  },
  updated: function() {
  	if(this.currentPage != this.lastPage || this.sortByCode != this.lastSortByCode){
  		
  		this.showSpinner = true;
  		
  		if(this.sortByCode != this.lastSortByCode){ this.currentPage = 1 }

  		this.lastPage = this.currentPage
  		this.lastSortByCode = this.sortByCode

  		if (!this.$session.exists()) {
  			this.$router.push('/')
  		}
  		else {
  			var username = this.$session.getAll().username
  			var password = this.$session.getAll().password

  			//const path = 'http://aws.kylesilverman.com:5000/machines?'
  			const path = 'http://localhost:5000/machines?'
  			const data = "username="+username+"&password="+password+"&page="+this.currentPage+"&sort="+this.sortByCode

  			this.$session.set('page', this.currentPage);
  			this.$session.set('sort', this.sortByCode);

  			this.$http.post(path+data).then(response => {
 
 				var body = response.body
 				this.numSystems = body.numSystems;
  				this.items = body.machines;
  				if(body.length === 0){
  					this.emptyBodyText = "There are no more systems to display. Please navigate to a previous page."
  				}else{
  					this.emptyBodyText = ""
  				}
  				this.showSpinner = false;
  			}).catch(error => {
  				console.log(this.$session.getAll())
  			})
  		}
  	}
  },
  methods: {
  	show_spin() {
    	this.showSpinner = true;
    },
    onHistoryClose(id) {
      this.$root.$emit('bv::hide::popover', 'popover_' + id);
    },
    onHistoryDisable(id) {
    	this.$root.$emit('bv::disable::popover', 'popover_' + id);
    },
    onHistoryShow(id) {
      /* This is called just before the popover is shown */
      /* Reset our popover "form" variables */
      this.history_items = [];
      for(var i =0; i < this.items.length; i++)
      {
      	if(this.items[i].serialNumberInserv != id)
      	{
      		this.onHistoryClose(this.items[i].serialNumberInserv);
      		this.onHistoryDisable(this.items[i].serialNumberInserv);
      	}
      }
      this.showHistorySpinner = true;
      var username = this.$session.getAll().username
  	  var password = this.$session.getAll().password
      const path = 'http://localhost:5000/history?'
	  const data = "username="+username+"&password="+password+"&sni="+id

	  this.$http.post(path+data).then(response => {

 			var body = response.body;
  			this.history_items = body;
  			this.showHistorySpinner = false;
  			this.$root.$emit('bv::enable::popover'); //enables all popovers after query

  		}).catch(error => {
  			console.log(this.$session.getAll())
  		})

    },
    doHistory(item_index, history_index, id) {
    	this.items[item_index] = this.history_items[history_index];
    	this.onHistoryClose(id);
    	this.$forceUpdate();
    },
  	onSearch(){
  	    this.isSearch = true;
  		this.searchInput = this.searchForm;
  		this.searchForm = "";

  	},
  	clearSearch(){
  		this.isSearch = false;
  	},
  	setSort(val){

  		if(val === 'fslh'){
  			this.sortByIcon = ['fas', 'sort-amount-up']
  			this.sortByCode = 'fslh'
  		}else if(val === 'fshl'){
  			this.sortByIcon = ['fas', 'sort-amount-down']
  			this.sortByCode = 'fshl'
  		}else if(val === 'snlh'){
  			this.sortByIcon = ['fas', 'sort-numeric-down']
  			this.sortByCode = 'snlh'
  		}else if(val === 'snhl'){
  			this.sortByIcon = ['fas', 'sort-numeric-up']
  			this.sortByCode = 'snhl'
  		}else if(val === 'cnaz'){
  			this.sortByIcon = ['fas', 'sort-alpha-down']
  			this.sortByCode = 'cnaz'
  		}else if(val === 'cnza'){
  			this.sortByIcon = ['fas', 'sort-alpha-up']
  			this.sortByCode = 'cnza'
  		}
  	},
  	sendInfo(machine, machine_index) {
        this.machine = machine;
        this.machine_index = machine_index;
        this.onHistoryClose(machine.serialNumberInserv)
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
