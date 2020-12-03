import { modifyMainView, ViewType, SyncStatus, postToServer } from "./common";
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
  protocol_title: modifyMainView((obj, val) => {
    obj.title = val;
    obj.$repr = val;
  }),
  protocol_overview: modifyMainView((obj, val) => {
    obj.overview = val;
  }),
  protocol_facility: modifyMainView((obj, { val }) => {
    obj.facility = val;
  }),
  protocol_inspectionDate: modifyMainView((obj, val) => {
    obj.inspection_date = val;
  }),
  protocol_inspector: modifyMainView((obj, { val }) => {
    obj.inspector = val;
  }),
  protocol_issuer: modifyMainView((obj, { val }) => {
    obj.issuer = val;
  }),
  protocol_attendees: modifyMainView((obj, val) => {
    obj.attendees = val;
  }),
  protocol_addEntry: modifyMainView(obj => {
    const entry = entryState();
    entry.$status |= SyncStatus.New;
    obj.entries.push(entry);
  }),
  protocol_removeEntry: modifyMainView((obj, index) => {
    obj.entries.splice(index, 1);
  }),
  protocol_prepareForSync: modifyMainView(obj => {
    obj.entries = obj.entries.filter(entry => (entry.$status & SyncStatus.Modified) !== 0);
    obj.entries.forEach((entry, i) => {
      entry.index = i;
      entry.flaws = entry.flaws.filter(flaw => (flaw.$status & SyncStatus.Modified) !== 0);
    });
  })
}

export const protocolGetters = {
  title(...args) {
    const getter = args[3];
    return getter.main.title;
  },
  overview(...args) {
    const getter = args[3];
    return getter.main.overview;
  },
  facility(...args) {
    const getter = args[3];
    return getter.main.facility;
  },
  inspectionDate(...args) {
    const getter = args[3];
    return getter.main.inspection_date;
  },
  inspector(...args) {
    const getter = args[3];
    return getter.main.inspector;
  },
  issuer(...args) {
    const getter = args[3];
    return getter.main.issuer;
  },
  attendees(...args) {
    const getter = args[3];
    return getter.main.attendees;
  },
  entries(...args) {
    const getter = args[3];
    return getter.main.entries;
  },
}

export const protocolActions = {
  store({ commit, rootGetters }) {
    commit("protocol_prepareForSync", null, { root: true });
    return postToServer(commit, rootGetters, "protocol", "main");
  },
}
