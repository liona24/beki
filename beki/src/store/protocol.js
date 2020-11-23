import { newProtocol, newEntry, SyncStatus } from './common.js'

export default {
  namespaced: true,
  state: newProtocol,
  mutations: {
    title(state, title) {
      state.status |= SyncStatus.Modified;
      state.value.title = title;
    },
    overview(state, overview) {
      state.status |= SyncStatus.Modified;
      state.value.overview = overview;
    },
    facility(state, facility) {
      state.status |= SyncStatus.Modified;
      state.value.facility = facility;
    },
    inspection_date(state, inspection_date) {
      state.status |= SyncStatus.Modified;
      state.value.inspection_date = inspection_date;
    },
    inspector(state, inspector) {
      state.status |= SyncStatus.Modified;
      state.value.inspector = inspector;
    },
    issuer(state, issuer) {
      state.status |= SyncStatus.Modified;
      state.value.issuer = issuer;
    },
    attendees(state, attendees) {
      state.status |= SyncStatus.Modified;
      state.value.attendees = attendees;
    },

    addEntry(state) {
      state.status |= SyncStatus.Modified;
      state.value.entries.push(newEntry());
    },
    removeEntry(state, index) {
      state.status |= SyncStatus.Modified;
      state.value.entries.splice(index, 1);
    }
  },
  actions: {
    load({ commit }) {
      console.log(commit);
    }
  }
};
