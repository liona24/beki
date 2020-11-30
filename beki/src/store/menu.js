import { SyncStatus, ViewType, modifyLatestView } from "./common";
import { protocolState } from './protocol'
import Vue from 'vue'

export function menuState() {
  return {
    $type: ViewType.MainMenu,
    $status: SyncStatus.Empty,
    $repr: "",
    selected: null,
    searchResults: [],
    droppedFiles: [],
    previewImages: {},
    isPreviewLoading: false,
    isLoading: false
  }
}

export const menuMutations = {
  menu_selected: modifyLatestView((obj, selected) => {
    obj.selected = selected;
  }),
  menu_droppedFiles: modifyLatestView((obj, droppedFiles) => {
    obj.droppedFiles = droppedFiles;
  }),
  menu_searchResults: modifyLatestView((obj, searchResults) => {
    obj.searchResults = searchResults;
  }),

  menu_removeDroppedFile: modifyLatestView((obj, name) => {
    const i = obj.droppedFiles.findIndex(file => file.name === name);
    if (i >= 0) {
      obj.droppedFiles.splice(i, 1);
    }
  }),
  menu_removePreviewImage: modifyLatestView((obj, name) => {
    Vue.delete(obj.previewImages, name);
  }),
  menu_updatePreviewImage: modifyLatestView((obj, { name, url }) => {
    obj.previewImages[name] = url;
  }),
  menu_isLoading: modifyLatestView((obj, val) => {
    obj.isLoading = val;
  }),
  menu_isPreviewLoading: modifyLatestView((obj, val) => {
    obj.isPreviewLoading = val;
  }),
  menu_clearSelectedFiles: modifyLatestView(obj => {
    obj.previewImages = {};
    obj.droppedFiles = [];
  })
}

export const menuGetters = {
  droppedFiles(...args) {
    const getter = args[3];
    return getter.currentView.droppedFiles;
  },
  selected(...args) {
    const getter = args[3];
    return getter.currentView.selected;
  },
  searchResults(...args) {
    const getter = args[3];
    return getter.currentView.searchResults;
  },
  previewImages(...args) {
    const getter = args[3];
    return getter.currentView.previewImages;
  },
  isPreviewLoading(...args) {
    const getter = args[3];
    return getter.currentView.isPreviewLoading;
  },
  isLoading(...args) {
    const getter = args[3];
    return getter.currentView.isLoading;
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
      commit('push', { view: protocolState() }, { root: true })
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
        commit('push', { view: protocolState() }, { root: true })
      }
    })
    .finally(() => {
      console.log("Upload done. TODO");
      commit('menu_isLoading', false, { root: true });
      // commit('push', { view: protocolState() }, { root: true })
    });
  }
}
