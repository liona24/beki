<template>
  <div>
    <b-field :label="legacy ? 'Archiv' : 'Aktuelle Protokolle'">
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
      <b-button type="is-dark" outlined expanded :disabled="!selected" @click="displayInNewTab">PDF erstellen</b-button>
    </b-field>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: "MenuSearchAndDisplay",
  props: {
    legacy: Boolean
  },
  data() {
    return {
      selected: null,
      isFetching: false,
      searchString: "",
      data: [],
    }
  },
  methods: {
    displayInNewTab() {
      if (this.selected) {
        const endpoint = `api/_render/${this.selected.id}${this.legacy ? '/legacy' : ''}`;
        window.open(endpoint);
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
          src: this.legacy ? "legacy_protocol" : "protocol"
      }).then(resp => {
        this.data = resp.body;
      }, () => {
        console.error("discover api unavailable");
      }).finally(() => {
        this.isFetching = false;
      });
    }, 500),
  }
}
</script>

<style>

</style>
