import { modifyLatestView, ViewType, SyncStatus, postToServer } from "./common";

export function inspectionStandardState() {
  return {
    $type: ViewType.InspectionStandard,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    din: "",
    description: "",
    has_version: "Nein",
  };
}

function updateRepr(obj) {
  obj.$repr = `DIN ${obj.has_version === 'Ja' ? '(V) ' : ''} ${obj.din} ${obj.description}`;
}

export const inspectionStandardMutations = {
  inspectionStandard_din: modifyLatestView((obj, val) => {
    obj.din = val;
    updateRepr(obj);
  }),
  inspectionStandard_description: modifyLatestView((obj, val) => {
    obj.description = val;
    updateRepr(obj);
  }),
  inspectionStandard_hasVersion: modifyLatestView((obj, val) => {
    obj.has_version = val;
    updateRepr(obj);
  }),
}

export const inspectionStandardGetters = {
  din(...args) {
    const getter = args[3];
    return getter.currentView.din;
  },
  description(...args) {
    const getter = args[3];
    return getter.currentView.description;
  },
  hasVersion(...args) {
    const getter = args[3];
    return getter.currentView.has_version;
  },
}

export const inspectionStandardActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "inspection_standard");
  }
}
