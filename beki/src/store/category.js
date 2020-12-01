import { modifyLatestView, ViewType, SyncStatus, postToServer } from "./common";

export function categoryState() {
  return {
    $type: ViewType.Category,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    name: "",
    inspection_standards: []
  };
}

export const categoryMutations = {
  category_name: modifyLatestView((obj, name) => {
    obj.name = name;
    obj.$repr = name;
  }),
  category_inspectionStandards: modifyLatestView((obj, { val }) => {
    obj.inspection_standards = val;
  }),
  category_updateInspectionStandard: modifyLatestView((obj, { i, val }) => {
    if (i >= 0) {
      obj.inspection_standards[i] = val;
    } else {
      obj.inspection_standards.push(val);
    }
  }),
  category_removeInspectionStandard: modifyLatestView((obj, i) => {
    obj.inspection_standards.splice(i, 1);
  }),
}

export const categoryGetters = {
  name(...args) {
    const getter = args[3];
    return getter.currentView.name;
  },
  inspectionStandards(...args) {
    const getter = args[3];
    return getter.currentView.inspection_standards;
  }
}

export const categoryActions = {
  store({ commit, rootGetters }) {
    return postToServer(commit, rootGetters, "category");
  }
}
