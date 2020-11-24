import { modifyLatestView, ViewType, SyncStatus } from "./common";

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

export const inspectionStandardMutations = {
  inspectionStandard_din: modifyLatestView((obj, val) => {
    obj.din = val;
  }),
  inspectionStandard_description: modifyLatestView((obj, val) => {
    obj.description = val;
  }),
  inspectionStandard_hasVersion: modifyLatestView((obj, val) => {
    obj.has_version = val;
  }),
}

export const categoryGetters = {
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

export const organizationActions = {
  store({ commit, rootGetters }) {
    return new Promise((resolve, reject) => {
      console.log("Store inspectionStandard");
      const obj = rootGetters.currentView;
      if ((obj.$status & SyncStatus.Modified) == 0) {
        commit('pop', { root: true });
        resolve(obj);
      } else {
        // TODO: push to server
      }

    });
  },
  discard({ commit }) {
    return new Promise(resolve => {
      console.log("Discard inspectionStandard");
      commit('pop', { root: true });
      resolve();
    })
  }
}
