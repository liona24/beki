<template>
  <div class="columns">
    <div class="column">
    <b-field label="Aktuelle Protokolle">
      <b-autocomplete placeholder="Suchen ..."
        v-model="searchString"

        type="search"
        icon="magnify"
        field="$repr"

        :data="data"
        :loading="isFetching"

        @select="updateSelection"
        @typing="fetchData"

        clearable
        expanded>
      </b-autocomplete>
    </b-field>

    <b-field>
      <b-button type="is-dark" outlined expanded :disabled="!selected" @click="displayInNewTab(selected)">PDF erstellen</b-button>
    </b-field>
    </div>
    <div class="column">
    <b-field label="Archiv">
      <b-autocomplete placeholder="Suchen ..."
        v-model="searchStringLegacy"

        type="search"
        icon="magnify"
        field="$repr"

        :data="dataLegacy"
        :loading="isFetchingLegacy"

        @select="updateSelectionLegacy"
        @typing="fetchDataLegacy"

        clearable
        expanded>
      </b-autocomplete>
    </b-field>

    <b-field>
      <b-button type="is-dark" outlined expanded :disabled="!selectedLegacy" @click="displayInNewTab(selectedLegacy)">PDF erstellen</b-button>
    </b-field>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: "MenuSearchAndDisplay",
  data() {
    return {
      selected: null,
      isFetching: false,
      searchString: "",
      data: [],
      selectedLegacy: null,
      isFetchingLegacy: false,
      searchStringLegacy: "",
      dataLegacy: [],
    }
  },
  methods: {
    displayInNewTab(selected) {
      if (selected) {
        window.open(`/api/_render/${selected.id}`);
      }
    },
    updateSelection(e) {
      this.selected = e;
    },
    fetchData: debounce(function(query) {
      if (query.length < 1) {
        this.data = [];
        return;
      }

      this.isFetching = true;

      this.$http.post("api/_discover", {
          q: query,
          src: "protocol"
      }).then(resp => {
        this.data = resp.body;
      }, () => {
        console.error("discover api unavailable");
      }).finally(() => {
        this.isFetching = false;
      });
    }, 500),
    updateSelectionLegacy(e) {
      this.selectedLegacy = e;
    },
    fetchDataLegacy: debounce(function(query) {
      if (query.length < 1) {
        this.dataLegacy = [];
        return;
      }

      this.isFetchingLegacy = true;

      this.$http.post("api/_discover", {
          q: query,
          src: "legacy_protocol"
      }).then(resp => {
        this.dataLegacy = resp.body;
      }, () => {
        console.error("discover api unavailable");
      }).finally(() => {
        this.isFetchingLegacy = false;
      });
    }, 500),
  }
}
</script>

<style>

</style>
