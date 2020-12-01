import { modifyLatestView, ViewType, SyncStatus, postToServer } from "./common";

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

function updateRepr(obj) {
  if (obj.name && obj.city) {
    obj.$repr = `${obj.name}, ${obj.city}`;
  } else {
    obj.$repr = obj.name;
  }
}

export const facilityMutations = {
  facility_name: modifyLatestView((obj, name) => {
    obj.name = name;
    updateRepr(obj);
  }),
  facility_street: modifyLatestView((obj, val) => {
    obj.street = val;
  }),
  facility_zipCode: modifyLatestView((obj, val) => {
    obj.zip_code = val;
  }),
  facility_city: modifyLatestView((obj, val) => {
    obj.city = val;
    updateRepr(obj);
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
    return postToServer(commit, rootGetters, "facility");
  }
}
