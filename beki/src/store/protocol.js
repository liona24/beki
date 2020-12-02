import { modifyLatestView, ViewType, SyncStatus, postToServer } from "./common";
import { organizationState } from './organization'
import { personState } from "./person";
import { facilityState } from "./facility";
import { entryState } from "./entry";

export function protocolState() {
  return {
    $type: ViewType.Protocol,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    title: "",
    overview: "",
    facility: facilityState(),
    inspection_date: "",
    inspector: personState(),
    issuer: organizationState(),
    attendees: "",
    entries: [],
  };
}

export const protocolMutations = {
  protocol_title: modifyLatestView((obj, val) => {
    obj.title = val;
    obj.$repr = val;
  }),
  protocol_overview: modifyLatestView((obj, val) => {
    obj.overview = val;
  }),
  protocol_facility: modifyLatestView((obj, { val }) => {
    obj.facility = val;
  }),
  protocol_inspectionDate: modifyLatestView((obj, val) => {
    obj.inspection_date = val;
  }),
  protocol_inspector: modifyLatestView((obj, { val }) => {
    obj.inspector = val;
  }),
  protocol_issuer: modifyLatestView((obj, { val }) => {
    obj.issuer = val;
  }),
  protocol_attendees: modifyLatestView((obj, val) => {
    obj.attendees = val;
  }),
  protocol_addEntry: modifyLatestView(obj => {
    const entry = entryState();
    entry.$status |= SyncStatus.New;
    obj.entries.push(entry);
  }),
  protocol_removeEntry: modifyLatestView((obj, index) => {
    obj.entries.splice(index, 1);
  }),
  protocol_syncIndices: modifyLatestView(obj => {
    obj.entries.forEach((entry, i) => {
      entry.index = i;
    });
  })
}

export const protocolGetters = {
  title(...args) {
    const getter = args[3];
    return getter.currentView.title;
  },
  overview(...args) {
    const getter = args[3];
    return getter.currentView.overview;
  },
  facility(...args) {
    const getter = args[3];
    return getter.currentView.facility;
  },
  inspectionDate(...args) {
    const getter = args[3];
    return getter.currentView.inspection_date;
  },
  inspector(...args) {
    const getter = args[3];
    return getter.currentView.inspector;
  },
  issuer(...args) {
    const getter = args[3];
    return getter.currentView.issuer;
  },
  attendees(...args) {
    const getter = args[3];
    return getter.currentView.attendees;
  },
  entries(...args) {
    const getter = args[3];
    return getter.currentView.entries;
  },
}

export const protocolActions = {
  store({ commit, rootGetters }) {
    commit("protocol_syncIndices", null, { root: true });
    return postToServer(commit, rootGetters, "protocol");
  },
}
