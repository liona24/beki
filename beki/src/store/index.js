import Vue from 'vue'
import Vuex from 'vuex'

import protocol from './protocol'
import tmp from './tmp'


Vue.use(Vuex);

export const store = new Vuex.Store({
  modules: {
    protocol: protocol,
    tmp: tmp
  }
});
