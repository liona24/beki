import { ViewType, SyncStatus } from "./common";
import { categoryState } from './category'
import { flawState } from './flaw'

export function entryState() {
  return {
    $type: ViewType.Entry,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    index: null,
    category: categoryState(),
    category_version: "",
    title: "",
    manufacturer: "",
    year_built: "",
    inspection_signs: "",
    manufacture_info_available: "Keine Angabe",
    easy_access: "Keine Angabe",
    flaws: [],
    _collapsed: false,
  };
}

function _modifyEntry(func) {
  return (state, param) => {
    const obj = state.views[state.views.length - 1];
    const entry = obj.entries[param.i];
    entry.$status |= SyncStatus.Modified;
    return func(entry, param);
  }
}

export const entryMutations = {
  entry_category: _modifyEntry((obj, { val }) => {
    obj.category = val;
  }),
  entry_categoryVersion: _modifyEntry((obj, { val }) => {
    obj.category_version = val;
  }),
  entry_title: _modifyEntry((obj, { val }) => {
    obj.title = val;
    obj.$repr = val;
  }),
  entry_manufacturer: _modifyEntry((obj, { val }) => {
    obj.manufacturer = val;
  }),
  entry_yearBuilt: _modifyEntry((obj, { val }) => {
    obj.year_built = val;
  }),
  entry_inspectionSigns: _modifyEntry((obj, { val }) => {
    obj.inspection_signs = val;
  }),
  entry_manufactureInfoAvailable: _modifyEntry((obj, { val }) => {
    obj.manufacture_info_available = val;
  }),
  entry_easyAccess: _modifyEntry((obj, { val }) => {
    obj.easy_access = val;
  }),
  entry_addFlaw: _modifyEntry(obj => {
    const flaw = flawState();
    flaw.$status |= SyncStatus.New;
    obj.flaws.push(flaw);
  }),

  entry_removeFlaw: (state, { entry, i }) => {
    const view = state.views[state.views.length - 1];
    const obj = view.entries[entry];
    obj.$status |= SyncStatus.Modified;
    obj.flaws.splice(i, 1);
  },
  entry_triggerCollapse: (state, { i }) => {
    const entry = state.views[state.views.length - 1].entries[i];
    entry._collapsed = !entry._collapsed;
  }
}
