import { ViewType, SyncStatus, modifyLatestView } from "./common";

export function flawState() {
  return {
    $type: ViewType.Flaw,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    title: "",
    img: "",
    notes: "",
    priority: ""
  };
}

export const flawMutations = {
  flaw_title: modifyLatestView((obj, { entry, i, val }) => {
    obj.entries[entry].flaws[i].title = val;
  }),
  flaw_img: modifyLatestView((obj, { entry, i, val }) => {
    obj.entries[entry].flaws[i].img = val;
  }),
  flaw_notes: modifyLatestView((obj, { entry, i, val }) => {
    obj.entries[entry].flaws[i].notes = val;
  }),
  flaw_priority: modifyLatestView((obj, { entry, i, val }) => {
    obj.entries[entry].flaws[i].priority = val;
  })
}
