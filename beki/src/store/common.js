export const SyncStatus = Object.freeze({
  Empty: 0,
  Modified: 1,
  New: 2,
  AwaitsConfirmation: 4,

  Lazy: 32,
  Stored: 64,
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

export function postToServer(commit, rootGetters, endpoint) {
  return new Promise((resolve, reject) => {
    const obj = rootGetters.currentView;
    if ((obj.$status & SyncStatus.Modified) == 0) {
      resolve(false);
    } else {
      const body = Object.assign({}, obj);
      fetch(`/api/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      })
      .then(resp => resp.json())
      .then(json => {
        if (json.errors?.length > 0) {
          reject(json.errors);
        } else {
          commit("updateId", { id: json.id }, { root: true });
          resolve(true);
        }
      }, () => {
        console.error("post api unavailable");
        reject([ { msg: "Verbindung zum Server nicht möglich!" } ]);
      });
    }
  });
}
