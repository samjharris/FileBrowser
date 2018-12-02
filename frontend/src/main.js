import Vue from 'vue';

import App from './App.vue';

import BootstrapVue from 'bootstrap-vue';

import router from './router';

import VueResource from 'vue-resource';

import VueSession from 'vue-session';

import TreeView from 'vue-json-tree-view';

import queryString from 'query-string';



import { library } from '@fortawesome/fontawesome-svg-core';

import { faFileDownload } from '@fortawesome/free-solid-svg-icons';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import { faHdd } from '@fortawesome/free-regular-svg-icons';

import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons'

library.add(faFileDownload, faHdd, faExclamationTriangle);

import VueChartkick from 'vue-chartkick'

import Chart from 'chart.js'

Vue.use(VueChartkick, {adapter: Chart})

library.add(faFileDownload, faHdd);

Vue.component('font-awesome-icon', FontAwesomeIcon);



Vue.config.productionTip = false;

Vue.use(queryString);

Vue.use(BootstrapVue);

Vue.use(VueResource);

Vue.use(VueSession);

Vue.use(TreeView);



Vue.http.options.xhr = {withCredentials: true};

Vue.http.options.crossOrigin = true;



const ACAH = [
	
	'Origin', 

	'Accept', 

	'Content-Type', 

	'Authorization', 

	'Access-Control-Allow-Origin'

];



Vue.http.headers.common['Content-Type'] = 'application/json';

Vue.http.headers.common['Accept'] = 'application/json';

Vue.http.headers.common['credentials'] = 'same-origin';

Vue.http.headers.common['Authorization'] = 'JsOnDeRulO';

Vue.http.headers.common['Access-Control-Allow-Origin'] = '*';

Vue.http.headers.common['Access-Control-Allow-Headers'] = ACAH.join(', ');



new Vue({
  
  router,
  
  render: h => h(App)

}).$mount('#app')