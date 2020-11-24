export const SyncStatus = Object.freeze({
  Empty: 0,
  Modified: 1,
  New: 2,
  AwaitsConfirmation: 4,
});

export const ViewType = Object.freeze({
  MainMenu: 0,
  Protocol: 1,
  Facility: 2,
  Organization: 3,
  Person: 4,
  InspectionStandard: 5,
  Category: 6,

  // These are merely placeholders since they are integrated into
  // the ProtocolView
  Entry: 7,
  Flaw: 8
});

export function modifyLatestView(func) {
  return (state, ...args) => {
    const obj = state.views[state.views.length - 1];
    obj.$status |= SyncStatus.Modified;
    return func(obj, ...args);
  }
}

export function newFlaw() {
  console.error("newFlaw not implemented");
  return {
    $type: ViewType.Flaw,
    id: null
  }
}
