import { modifyOverlayView, ViewType, SyncStatus, postToServer } from "./common";
import { organizationState } from './organization'

export function personState() {
  return {
    $type: ViewType.Person,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    name: "",
    first_name: "",
    email: "",
    organization: organizationState(),
  }
}

function updateRepr(obj) {
  if (obj.name && obj.first_name) {
    obj.$repr = `${obj.name}, ${obj.first_name}`;
  } else {
    obj.$repr = obj.name;
  }
}

export const personMutations = {
  person_name: modifyOverlayView((obj, name) => {
    obj.name = name;
    updateRepr(obj);
  }),
  person_firstName: modifyOverlayView((obj, val) => {
    obj.first_name = val;
    updateRepr(obj);
  }),
  person_email: modifyOverlayView((obj, val) => {
    obj.email = val;
  }),
  person_organization: modifyOverlayView((obj, { val }) => {
    obj.organization = val;
  }),
}

export const personGetters = {
  name(...args) {
    const getter = args[3];
    return getter.overlay.name;
  },
  firstName(...args) {
    const getter = args[3];
    return getter.overlay.first_name;
  },
  email(...args) {
    const getter = args[3];
    return getter.overlay.email;
  },
  organization(...args) {
    const getter = args[3];
    return getter.overlay.organization;
  },
}

export const personActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "person", "overlay");
  },
}
