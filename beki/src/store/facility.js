import { modifyOverlayView, ViewType, SyncStatus, postToServer } from "./common";

export function facilityState() {
  return {
    $type: ViewType.Facility,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    name: "",
    street: "",
    zip_code: "",
    city: "",
    picture: ""
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
  facility_name: modifyOverlayView((obj, name) => {
    obj.name = name;
    updateRepr(obj);
  }),
  facility_street: modifyOverlayView((obj, val) => {
    obj.street = val;
  }),
  facility_zipCode: modifyOverlayView((obj, val) => {
    obj.zip_code = val;
  }),
  facility_city: modifyOverlayView((obj, val) => {
    obj.city = val;
    updateRepr(obj);
  }),
  facility_picture: modifyOverlayView((obj, val) => {
    obj.picture = val;
  }),
}

export const facilityGetters = {
  name(...args) {
    const getter = args[3];
    return getter.overlay.name;
  },
  street(...args) {
    const getter = args[3];
    return getter.overlay.street;
  },
  zipCode(...args) {
    const getter = args[3];
    return getter.overlay.zip_code;
  },
  city(...args) {
    const getter = args[3];
    return getter.overlay.city;
  },
  picture(...args) {
    const getter = args[3];
    return getter.overlay.picture;
  },
}

export const facilityActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "facility", "overlay");
  }
}
