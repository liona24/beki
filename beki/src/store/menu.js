import { SyncStatus, ViewType, modifyMainView } from "./common";
import { protocolState } from './protocol'
import { wizardState } from './wizard'
import Vue from 'vue'
import { SnackbarProgrammatic as Snackbar } from 'buefy'
import { chunk } from 'lodash'

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
    commit('menu_isLoading', true, { root: true });
    const tasks = getters.droppedFiles.map(
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
    );

    tasks.reduce((promiseChain, currentTask) => {
      return promiseChain.then(chainResults =>
          currentTask.then(currentResult =>
          [ ...chainResults, currentResult ]
        )
      );
    }, Promise.resolve([]))
    .then(() => commit('menu_isLoading', false, { root: true }));

    // parallel version (slows down the browser quite a lot.)
    // Promise.all(tasks).then(() => commit('menu_isLoading', false, { root: true }));
  },
  newProtocol({ commit, getters, dispatch }) {
    if (getters.droppedFiles.length === 0) {
      const view = protocolState();
      view.$status |= SyncStatus.New;
      commit('push_main', { view: view, callback: "menu_currentPreviewId", args: null }, { root: true });
      return;
    }

    commit('menu_isLoading', true, { root: true });

    const images = [];

    // be nice to the server
    const chunks = chunk(getters.droppedFiles, 2);
    const uploads = chunks.map(files => new Promise((resolve, reject) => {
      const data = new FormData();
      files.forEach(file => {
        data.append(file.name, file);
      });

      fetch("/api/_upload", {
        method: "POST",
        body: data
      })
      .then(resp => resp.json())
      .then(json => {
        images.push(...Object.keys(json).map(k => json[k]));
        resolve();
      })
      .catch(reject);
    }));

    Promise.all(uploads).then(() => {
      if (images.length === 0) {
        throw Error();
      }
      commit('menu_clearSelectedFiles', null, { root: true });
      commit('menu_isLoading', false, { root: true });
      const wizard = wizardState();
      wizard.images = images;
      commit('push_main', { view: wizard }, { root: true });
      dispatch("wizard/preprocess", null, { root: true });
    })
    .catch(() => {
      commit("menu_clearSelectedFiles", null, { root: true });
      commit('menu_isLoading', false, { root: true });
      Snackbar.open({
        duration: 6000,
        message: `Fehler: Bilder konnten nicht hochgeladen werden!`,
        type: 'is-danger',
        queue: false
      });
    });
  },
  editProtocol({ commit }, protocol) {
    commit("menu_isLoading", true, { root: true });
    fetch(`/api/protocol/${protocol.id}/recursive`)
    .then(resp => resp.json())
    .then(json => {
      commit('menu_isLoading', false, { root: true });
      commit('menu_clearSelectedFiles', null, { root: true });
      commit('push_main', { view: json, callback: "menu_currentPreviewId", args: null }, { root: true });
    })
    .catch(() => {
      commit('menu_isLoading', false, { root: true });
      Snackbar.open({
        duration: 6000,
        message: `Fehler: Protokoll konnte nicht geladen werden!`,
        type: 'is-danger',
        queue: false
      });
    });
  }
}
