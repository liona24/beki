import { modifyOverlayView, ViewType, SyncStatus, postToServer } from "./common";

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
  const descMaxLen = 10
  let desc = obj.description;
  if (desc.len >= descMaxLen) {
    desc = desc.substring(0, descMaxLen - 2) + "..";
  }
  obj.$repr = `DIN ${obj.has_version === 'Ja' ? '(V) ' : ''} ${obj.din} ${desc}`;
}

export const inspectionStandardMutations = {
  inspectionStandard_din: modifyOverlayView((obj, val) => {
    obj.din = val;
    updateRepr(obj);
  }),
  inspectionStandard_description: modifyOverlayView((obj, val) => {
    obj.description = val;
    updateRepr(obj);
  }),
  inspectionStandard_hasVersion: modifyOverlayView((obj, val) => {
    obj.has_version = val;
    updateRepr(obj);
  }),
}

export const inspectionStandardGetters = {
  din(...args) {
    const getter = args[3];
    return getter.overlay.din;
  },
  description(...args) {
    const getter = args[3];
    return getter.overlay.description;
  },
  hasVersion(...args) {
    const getter = args[3];
    return getter.overlay.has_version;
  },
}

export const inspectionStandardActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "inspection_standard", "overlay");
  }
}
