import { modifyLatestView, ViewType, SyncStatus } from "./common";
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

export const entryMutations = {
  entry_category: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].category = val;
  }),
  entry_categoryVersion: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].category_version = val;
  }),
  entry_title: modifyLatestView((obj, { i, val }) => {
    const entry = obj.entries[i];
    entry.title = val;
    entry.$repr = val;
  }),
  entry_manufacturer: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].manufacturer = val;
  }),
  entry_yearBuilt: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].year_built = val;
  }),
  entry_inspectionSigns: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].inspection_signs = val;
  }),
  entry_manufactureInfoAvailable: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].manufacture_info_available = val;
  }),
  entry_easyAccess: modifyLatestView((obj, { i, val }) => {
    obj.entries[i].easy_access = val;
  }),
  entry_addFlaw: modifyLatestView((obj, { i }) => {
    obj.entries[i].flaws.push(flawState());
  }),
  entry_removeFlaw: modifyLatestView((obj, { entry, i }) => {
    obj.entries[entry].flaws.splice(i, 1);
  }),
  entry_triggerCollapse: (state, { i }) => {
    const entry = state.views[state.views.length - 1].entries[i];
    entry._collapsed = !entry._collapsed;
  }
}
