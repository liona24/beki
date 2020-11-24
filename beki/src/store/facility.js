import { modifyLatestView, ViewType, SyncStatus } from "./common";

export function facilityState() {
  return {
    $type: ViewType.Facility,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    name: "",
    street: "",
    zip_code: "",
    city: ""
  };
}

export const facilityMutations = {
  facility_name: modifyLatestView((obj, name) => {
    obj.name = name;
  }),
  facility_street: modifyLatestView((obj, val) => {
    obj.street = val;
  }),
  facility_zipCode: modifyLatestView((obj, val) => {
    obj.zip_code = val;
  }),
  facility_city: modifyLatestView((obj, val) => {
    obj.city = val;
  }),
}

export const facilityGetters = {
  name(...args) {
    const getter = args[3];
    return getter.currentView.name;
  },
  street(...args) {
    const getter = args[3];
    return getter.currentView.street;
  },
  zipCode(...args) {
    const getter = args[3];
    return getter.currentView.zip_code;
  },
  city(...args) {
    const getter = args[3];
    return getter.currentView.city;
  },
}

export const facilityActions = {
  store({ commit, rootGetters }) {
    return new Promise((resolve, reject) => {
      console.log("Store facility");
      const obj = rootGetters.currentView;
      if ((obj.$status & SyncStatus.Modified) == 0) {
        commit('pop', { root: true });
        resolve(obj);
      } else {
        // TODO: push to server
        console.log(reject);
      }

    });
  },
  discard({ commit }) {
    return new Promise(resolve => {
      console.log("Discard facility");
      commit('pop', { root: true });
      resolve();
    })
  }
}
