import Vue from 'vue'
import Buefy from 'buefy'
import VueResource from 'vue-resource'
import App from './App.vue'
import { store } from './store/index.js'

import 'buefy/dist/buefy.css'

Vue.config.productionTip = false

Vue.use(Buefy, {});
Vue.use(VueResource, {
  root: "",
  headers: {}
});

new Vue({
  render: h => h(App),
  store: store
}).$mount('#app')
