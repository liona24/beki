import { SyncStatus, ViewType, modifyMainView } from "./common";
import { protocolState } from './protocol'
import Vue from 'vue'

export function menuState() {
  return {
    $type: ViewType.MainMenu,
    $status: SyncStatus.Empty,
    $repr: "",
    droppedFiles: [],
    previewImages: {},
    isPreviewLoading: false,
    isLoading: false,
    currentPreviewId: null
  }
}

export const menuMutations = {
  menu_selected: modifyMainView((obj, selected) => {
    obj.selected = selected;
  }),
  menu_droppedFiles: modifyMainView((obj, droppedFiles) => {
    obj.droppedFiles = droppedFiles;
  }),
  menu_searchResults: modifyMainView((obj, searchResults) => {
    obj.searchResults = searchResults;
  }),

  menu_removeDroppedFile: modifyMainView((obj, name) => {
    const i = obj.droppedFiles.findIndex(file => file.name === name);
    if (i >= 0) {
      obj.droppedFiles.splice(i, 1);
    }
  }),
  menu_removePreviewImage: modifyMainView((obj, name) => {
    Vue.delete(obj.previewImages, name);
  }),
  menu_updatePreviewImage: modifyMainView((obj, { name, url }) => {
    obj.previewImages[name] = url;
  }),
  menu_isLoading: modifyMainView((obj, val) => {
    obj.isLoading = val;
  }),
  menu_isPreviewLoading: modifyMainView((obj, val) => {
    obj.isPreviewLoading = val;
  }),
  menu_clearSelectedFiles: modifyMainView(obj => {
    obj.previewImages = {};
    obj.droppedFiles = [];
  }),
  menu_currentPreviewId: modifyMainView((obj, { val }) => {
    obj.currentPreviewId = val?.id;
  })
}

export const menuGetters = {
  droppedFiles(...args) {
    const getter = args[3];
    return getter.main.droppedFiles;
  },
  previewImages(...args) {
    const getter = args[3];
    return getter.main.previewImages;
  },
  isPreviewLoading(...args) {
    const getter = args[3];
    return getter.main.isPreviewLoading;
  },
  isLoading(...args) {
    const getter = args[3];
    return getter.main.isLoading;
  },
  currentPreviewId(...args) {
    const getter = args[3];
    return getter.main.currentPreviewId;
  }
}

export const menuActions = {
  loadPreviews({ commit, getters }) {
    commit('menu_isPreviewLoading', true, { root: true });

    Promise.all(
      getters.droppedFiles.map(
        file => new Promise(resolve => {
          const reader = new FileReader();
          reader.onload = e => {
            commit('menu_updatePreviewImage', {
              name: file.name,
              url: e.target.result
            }, { root: true });
            resolve();
          };
          reader.readAsDataURL(file);
        })
      )
    ).then(() => commit('menu_isPreviewLoading', false, { root: true }));
  },
  newProtocol({ commit, getters }) {
    if (getters.droppedFiles.length === 0) {
      const view = protocolState();
      view.$status |= SyncStatus.New;
      commit('push_main', { view: view, callback: "menu_currentPreviewId", args: null }, { root: true });
      return;
    }

    commit('menu_isLoading', true, { root: true });
    const data = new FormData();
    getters.droppedFiles.forEach(file => {
      data.append(file.name, file);
    });
    fetch("/api/_upload", {
      method: "POST",
      body: data
    })
    .then(resp => resp.json())
    .then(json => {
      commit('menu_clearSelectedFiles', null, { root: true });
      console.log("upload successful", json);
      if (json === "ASDF") {
        // happy linter
        // do not forget about the SyncStatus.New! Otherwise the server
        // might reject changes
        commit('push_main', { view: protocolState() }, { root: true })
      }
    })
    .finally(() => {
      console.log("Upload done. TODO");
      commit('menu_isLoading', false, { root: true });
      // commit('push_main', { view: protocolState() }, { root: true })
    });
  }
}
