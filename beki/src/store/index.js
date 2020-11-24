import Vue from 'vue'
import Vuex from 'vuex'

import { menuState, menuGetters, menuMutations, menuActions } from './menu'
import { protocolGetters, protocolActions, protocolMutations } from './protocol'
import { facilityGetters, facilityMutations, facilityActions } from './facility'
import { organizationGetters, organizationMutations, organizationActions } from './organization'
import { categoryGetters, categoryMutations, categoryActions } from './category'
import { inspectionStandardGetters, inspectionStandardMutations, inspectionStandardActions } from './inspection_standard'
import { personGetters, personMutations, personActions } from './person'

import { entryMutations } from './entry'

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
    ...protocolMutations,
    ...facilityMutations,
    ...organizationMutations,
    ...categoryMutations,
    ...inspectionStandardMutations,
    ...personMutations,
    ...entryMutations,
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
    facility: {
      namespaced: true,
      getters: {
        ...facilityGetters
      },
      actions: {
        ...facilityActions
      }
    },
    organization: {
      namespaced: true,
      getters: {
        ...organizationGetters
      },
      actions: {
        ...organizationActions
      }
    },
    category: {
      namespaced: true,
      getters: {
        ...categoryGetters
      },
      actions: {
        ...categoryActions
      }
    },
    inspectionStandard: {
      namespaced: true,
      getters: {
        ...inspectionStandardGetters
      },
      actions: {
        ...inspectionStandardActions
      }
    },
    person: {
      namespaced: true,
      getters: {
        ...personGetters
      },
      actions: {
        ...personActions
      }
    },
  }

});
