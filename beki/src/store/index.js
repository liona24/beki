import Vue from 'vue'
import Vuex from 'vuex'

import { menuState, menuGetters, menuMutations, menuActions } from './menu'
import { protocolGetters, protocolActions, protocolMutations } from './protocol'
import { facilityGetters, facilityMutations, facilityActions } from './facility'
import { organizationGetters, organizationMutations, organizationActions } from './organization'
import { categoryGetters, categoryMutations, categoryActions } from './category'
import { inspectionStandardGetters, inspectionStandardMutations, inspectionStandardActions } from './inspection_standard'
import { personGetters, personMutations, personActions } from './person'
import { wizardActions, wizardGetters, wizardMutations } from './wizard'

import { entryMutations } from './entry'
import { flawMutations } from './flaw'
import { SyncStatus } from './common'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    main: {
      views: [
        menuState(),
      ],
      pop_callbacks: []
    },
    overlay: {
      views: [],
      pop_callbacks: []
    }
  },
  mutations: {
    push_main(state, { view, callback, args }) {
      state.main.pop_callbacks.push({ callback: callback, args: args });
      state.main.views.push(view);
    },
    push_overlay(state, { view, callback, args }) {
      state.overlay.pop_callbacks.push({ callback: callback, args: args });
      state.overlay.views.push(view);
    },
    updateId(state, { window, id }) {
      const obj = state[window].views[state[window].views.length - 1];
      if (id !== undefined && id !== null) {
        obj.$status &= ~(SyncStatus.New | SyncStatus.Modified);
        obj.$status |= SyncStatus.Stored;
        obj.id = id;
      } else {
        obj.$status &= ~(SyncStatus.Stored | SyncStatus.Modified | SyncStatus.Lazy);
        obj.$status |= SyncStatus.New;
      }
    },
    pop_main(state) {
      state.main.views.pop();
      state.main.pop_callbacks.pop();
    },
    pop_overlay(state) {
      state.overlay.views.pop();
      state.overlay.pop_callbacks.pop();
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
    ...wizardMutations
  },
  actions: {
    back_main({ commit, getters }, { discard }) {
      const obj = getters.main;
      const { callback, args } = getters.mainCallback;
      commit("pop_main");
      if (!discard && callback) {
        commit(callback, { val: obj, ...args });
      }
    },
    back_overlay({ commit, getters }, { discard }) {
      const obj = getters.overlay;
      const { callback, args } = getters.overlayCallback;
      commit("pop_overlay");
      if (!discard && callback) {
        commit(callback, { val: obj, ...args });
      }
    },
  },
  getters: {
    mainViewType(state) {
      return state.main.views[state.main.views.length - 1].$type;
    },
    main(state) {
      return state.main.views[state.main.views.length - 1];
    },
    mainStatus(state) {
      return state.main.views[state.main.views.length - 1].$status;
    },
    mainCallback(state) {
      return state.main.pop_callbacks[state.main.pop_callbacks.length - 1];
    },

    overlayViewType(state) {
      return state.overlay.views[state.overlay.views.length - 1]?.$type;
    },
    overlay(state) {
      return state.overlay.views[state.overlay.views.length - 1];
    },
    overlayStatus(state) {
      return state.overlay.views[state.overlay.views.length - 1]?.$status;
    },
    overlayCallback(state) {
      return state.overlay.pop_callbacks[state.overlay.pop_callbacks.length - 1];
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
    wizard: {
      namespaced: true,
      getters: {
        ...wizardGetters
      },
      actions: {
        ...wizardActions
      }
    }
  }

});
