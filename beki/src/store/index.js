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
import { flawMutations } from './flaw'
import { SyncStatus } from './common'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    views: [
      menuState(),
    ],
    pop_callbacks: []
  },
  mutations: {
    push(state, { view, callback, args }) {
      state.pop_callbacks.push({ callback: callback, args: args });
      state.views.push(view);
    },
    updateId(state, { id }) {
      const obj = state.views[state.views.length - 1];
      if (id !== undefined && id !== null) {
        obj.$status &= ~(SyncStatus.New | SyncStatus.Modified);
        obj.$status |= SyncStatus.Stored;
        obj.id = id;
      } else {
        obj.$status &= ~(SyncStatus.Stored | SyncStatus.Modified | SyncStatus.Lazy);
        obj.$status |= SyncStatus.New;
      }
    },
    pop_view(state) {
      state.views.pop();
      state.pop_callbacks.pop();
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
    ...flawMutations,
  },
  actions: {
    back({ commit, getters }, { discard }) {
      const obj = getters.currentView;
      const { callback, args } = getters.currentCallback;
      commit("pop_view");
      if (!discard && callback) {
        commit(callback, { val: obj, ...args });
      }
    },
  },
  getters: {
    currentViewType(state) {
      return state.views[state.views.length - 1].$type;
    },
    currentView(state) {
      return state.views[state.views.length - 1];
    },
    currentStatus(state) {
      return state.views[state.views.length - 1].$status;
    },
    currentCallback(state) {
      return state.pop_callbacks[state.pop_callbacks.length - 1];
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
