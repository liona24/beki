import { newFacility, newCategory, newInspectionStandard, newPerson, newOrganization, SyncStatus } from './common'

// this one is a simple solution to track modal state:
// Since there can only ever be one modal of each type open at a time
// we simply export state for each of them here
// this temporary state can then be synced to the server
// This solution does not scale particularly well, but
// it is simple.

export default {
  namespaced: true,
  modules: {
    organization: {
      namespaced: true,
      state: newOrganization,
      mutations: {
        name(state, name) {
          state.status |= SyncStatus.Modified;
          state.value.name = name;
        },
        street(state, street) {
          state.status |= SyncStatus.Modified;
          state.value.street = street;
        },
        zip_code(state, zip_code) {
          state.status |= SyncStatus.Modified;
          state.value.zip_code = zip_code;
        },
        city(state, city) {
          state.status |= SyncStatus.Modified;
          state.value.city = city;
        },
      }
    },
    facility: {
      namespaced: true,
      state: newFacility
    },
    person: {
      namespaced: true,
      state: newPerson,
    },
    inspection_standard: {
      namespaced: true,
      state: newInspectionStandard
    },
    category: {
      namespaced: true,
      state: newCategory
    },
  },

  state: () => {
    return {
      organizations: [],
    }
  },
  mutations: {
    addOrganization(state, org) {
      console.log("TODO, remove this", org);
      state.organizations.push(org);
    }
  },
  actions: {
    async addOrganization({ commit }, org) {
      console.log("TODO, remove this", org);
      return new Promise(resolve => {
        setTimeout(() => {
          commit("addOrganization", org);
          resolve(org);
        }, 1000);
      });
    }
  }
}
