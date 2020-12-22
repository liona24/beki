<template>
  <div>
    <b-field label="Suchen">
      <b-autocomplete placeholder="Suchen ..."
        v-model="searchString"

        type="search"
        icon="search"
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
      <b-button type="is-dark" outlined expanded :disabled="!selected" @click="load">Bearbeiten</b-button>
    </b-field>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'
export default {
  name: "MenuEdit",
  data() {
    return {
      selected: null,
      isFetching: false,
      searchString: "",
      data: [],
    }
  },
  methods: {
    load() {
      if (!this.selected) {
        return;
      }

      this.$store.dispatch("menu/editProtocol", this.selected)
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
  }
}
</script>

<style>

</style>
