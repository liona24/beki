import { modifyOverlayView, ViewType, SyncStatus, postToServer } from "./common";

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
  organization_name: modifyOverlayView((obj, name) => {
    obj.name = name;
    updateRepr(obj);
  }),
  organization_street: modifyOverlayView((obj, street) => {
    obj.street = street;
  }),
  organization_zipCode: modifyOverlayView((obj, zipcode) => {
    obj.zip_code = zipcode;
  }),
  organization_city: modifyOverlayView((obj, city) => {
    obj.city = city;
    updateRepr(obj);
  }),
}

export const organizationGetters = {
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
}

export const organizationActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "organization", "overlay");
  },
}
