import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFileDownload } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHdd } from '@fortawesome/free-regular-svg-icons'
<<<<<<< HEAD
import VueResource from 'vue-resource'
import router from './router'

=======
import router from './router'
>>>>>>> 500cdad8f7cc9c8d850dcfc7a4e8f1a4283b7fc2

library.add(faFileDownload, faHdd)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(VueResource);

new Vue({
<<<<<<< HEAD
	router,
  render: h => h(App),
=======
  router,
  render: h => h(App)
>>>>>>> 500cdad8f7cc9c8d850dcfc7a4e8f1a4283b7fc2
}).$mount('#app')
