import Vue from 'vue'
import Buefy from 'buefy'
import VueResource from 'vue-resource'
import App from './App.vue'
import { store } from './store/index.js'
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCheckCircle, faExclamationTriangle, faCloudUploadAlt, faEye, faPlus,
  faFile, faArchive, faTrash, faEdit, faSearch, faTimes, faChevronDown, faChevronUp,
  faHome, faChevronRight, faCheck, faFileUpload, faTags, faAsterisk, faTimesCircle }
  from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import 'buefy/dist/buefy.css'

library.add(faCheckCircle, faExclamationTriangle, faCloudUploadAlt, faEye, faPlus,
  faFile, faArchive, faTrash, faEdit, faSearch, faTimes, faChevronDown, faChevronUp,
  faHome, faChevronRight, faCheck, faFileUpload, faTags, faAsterisk, faTimesCircle );
Vue.component('vue-fontawesome', FontAwesomeIcon);

Vue.config.productionTip = false

Vue.use(Buefy, {
  defaultIconPack: 'fas',
  defaultIconComponent: 'vue-fontawesome'
});
Vue.use(VueResource, {
  root: "",
  headers: {}
});

new Vue({
  render: h => h(App),
  store: store
}).$mount('#app')
