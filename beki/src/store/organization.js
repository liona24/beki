import { modifyLatestView, ViewType, SyncStatus } from "./common";

export function organizationState() {
  return {
    $type: ViewType.Organization,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    name: "",
    street: "",
    zip_code: "",
    city: ""
  }
}

function updateRepr(obj) {
  if (obj.name && obj.city) {
    obj.$repr = `${obj.name}, ${obj.city}`;
  } else {
    obj.$repr = obj.name;
  }
}

export const organizationMutations = {
  organization_name: modifyLatestView((obj, name) => {
    obj.name = name;
    updateRepr(obj);
  }),
  organization_street: modifyLatestView((obj, street) => {
    obj.street = street;
  }),
  organization_zipCode: modifyLatestView((obj, zipcode) => {
    obj.zip_code = zipcode;
  }),
  organization_city: modifyLatestView((obj, city) => {
    obj.city = city;
    updateRepr(obj);
  }),
}

export const organizationGetters = {
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

export const organizationActions = {
  store({ commit, rootGetters }) {
    return new Promise((resolve, reject) => {
      console.log("Store organization");
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
      console.log("Discard organization");
      commit('pop', { root: true });
      resolve();
    })
  }
}