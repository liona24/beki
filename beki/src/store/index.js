import Vue from 'vue'
import Vuex from 'vuex'

import { menuState, menuGetters, menuMutations, menuActions } from './menu'
import { protocolGetters, protocolActions, protocolMutations } from './protocol'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    views: [
      menuState()
    ]
  },
  mutations: {
    push(state, view) {
      state.views.push(view);
    },
    pop(state, count = 1) {
      state.views.splice(state.views.length - count, count);
    },
    // sadly we cannot scope the mutations easily
    ...menuMutations,
    ...protocolMutations
  },
  getters: {
    currentViewType(state) {
      return state.views[state.views.length - 1].$type;
    },
    currentView(state) {
      return state.views[state.views.length - 1];
    }
  },

  modules: {
    menu: {
      namespaced: true,
      getters: {
        ...menuGetters
      },
      actions: {
        ...menuActions
      }
    },
    protocol: {
      namespaced: true,
      getters: {
        ...protocolGetters
      },
      actions: {
        ...protocolActions
      }
    },
  }

});
