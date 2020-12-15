import { SyncStatus, ViewType, modifyMainView } from "./common";
import { facilityState } from "./facility";

export function wizardState() {
  return {
    $type: ViewType.Wizard,
    $status: SyncStatus.Empty,
    $repr: "",
    isPreprocessingWorking: true,
    facility: facilityState(),
    images: [],
  }
}

export const wizardMutations = {
  wizard_facility: modifyMainView((obj, { val }) => {
    obj.facility = val;
  }),
  wizard_preprocessingFinished: modifyMainView(obj => {
    obj.isPreprocessingWorking = false;
  }),
}

export const wizardGetters = {
  facility(...args) {
    const getter = args[3];
    return getter.main.facility;
  },
  images(...args) {
    const getter = args[3];
    return getter.main.images;
  },
  isPreprocessingWorking(...args) {
    const getter = args[3];
    return getter.main.isPreprocessingWorking;
  }
}

export const wizardActions = {
  preprocess({ commit, getters }) {
    const body = JSON.stringify({ images: getters.images });
    const n_trials = 2;
    const attemptPreprocessing = trial => {
      const retry = () => {
        console.log(`Preprocessing failed. Trying again. (${trial + 1}/${n_trials})`);
        if (trial + 1 < n_trials) {
          attemptPreprocessing(trial + 1);
        } else {
          console.error("Preprocessing failed.");
          commit("wizard_preprocessingFinished", null, { root: true });
        }
      };

      fetch("/api/_imaging/preprocess", {
        method: "POST",
        body: body,
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(resp => resp.json())
      .then(json => {
        if (json.errors?.length !== 0) {
          console.error(json.errors);
          retry();
        } else {
          commit("wizard_preprocessingFinished", null, { root: true });
        }
      })
      .catch(retry);
    };
    attemptPreprocessing(0);
  }
}
