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

Vue.http.options.xhr = {withCredentials: true}
Vue.http.options.crossOrigin = true


Vue.http.headers.common['Content-Type'] = 'application/json';
Vue.http.headers.common['Accept'] = 'application/json';
Vue.http.headers.common['credentials'] = 'same-origin';
Vue.http.headers.common['Authorization'] = 'JsOnDeRulO';
Vue.http.headers.common['Access-Control-Allow-Origin'] = '*'
Vue.http.headers.common['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization, Access-Control-Allow-Origin'

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
