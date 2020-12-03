import { ViewType, SyncStatus } from "./common";

export function flawState() {
  return {
    $type: ViewType.Flaw,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    title: "",
    picture: "",
    notes: "",
    priority: ""
  };
}

function _modifyFlaw(func) {
  return (state, param) => {
    const obj = state.main.views[state.main.views.length - 1];
    const entry = obj.entries[param.entry];
    const flaw = entry.flaws[param.i];
    flaw.$status |= SyncStatus.Modified;
    return func(flaw, param);
  }
}

export const flawMutations = {
  flaw_title: _modifyFlaw((obj, { val }) => {
    obj.title = val;
    obj.$repr = val;
  }),
  flaw_picture: _modifyFlaw((obj, { val }) => {
    obj.picture = val;
  }),
  flaw_notes: _modifyFlaw((obj, { val }) => {
    obj.notes = val;
  }),
  flaw_priority: _modifyFlaw((obj, { val }) => {
    obj.priority = val;
  })
}
