import { modifyLatestView, ViewType, SyncStatus } from "./common";
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

export const personMutations = {
  person_name: modifyLatestView((obj, name) => {
    obj.name = name;
  }),
  person_firstName: modifyLatestView((obj, val) => {
    obj.first_name = val;
  }),
  person_email: modifyLatestView((obj, val) => {
    obj.email = val;
  }),
  person_organization: modifyLatestView((obj, val) => {
    obj.organization = val;
  }),
}

export const personGetters = {
  name(...args) {
    const getter = args[3];
    return getter.currentView.name;
  },
  firstName(...args) {
    const getter = args[3];
    return getter.currentView.firstName;
  },
  email(...args) {
    const getter = args[3];
    return getter.currentView.email;
  },
  organization(...args) {
    const getter = args[3];
    return getter.currentView.organization;
  },
}

export const personActions = {
  store({ commit, rootGetters }) {
    return new Promise((resolve, reject) => {
      console.log("Store person");
      const obj = rootGetters.currentView;
      if ((obj.$status & SyncStatus.Modified) == 0) {
        commit('pop', { root: true });
        resolve(obj);
      } else {
        console.log(reject);
        // TODO: push to server
      }

    });
  },
  discard({ commit }) {
    return new Promise(resolve => {
      console.log("Discard person");
      commit('pop', { root: true });
      resolve();
    })
  }
}
