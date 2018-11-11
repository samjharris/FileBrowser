import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFileDownload } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHdd } from '@fortawesome/free-regular-svg-icons'
import router from './router'
import VueResource from 'vue-resource'
import VueSession from 'vue-session'

library.add(faFileDownload, faHdd)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(VueSession);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
