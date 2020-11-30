<template>
  <div class="block">
    <b-field horizontal>
      <b-autocomplete
        :value="value"
        @input="updateValue"

        :data="data"
        :loading="isFetching"
        @typing="fetchData"

        placeholder="..."
        clearable
        :required="required"
        @select="updateValue">
        <template slot="empty">Keine Übereinstimmung</template>
      </b-autocomplete>
      <template slot="label">
        <slot>
          <span class="has-text-danger">TODO a label is missing</span>
        </slot>
      </template>
    </b-field>
  </div>
</template>

<script>
import { debounce } from 'lodash'

export default {
  name: "AutocompleteText",
  props: {
    required: {
      type: Boolean,
      default: false
    },
    value: String,
    requestSrc: String,
    requestKey: String
  },
  data() {
    return {
      data: [],
      isFetching: false,
    }
  },
  methods: {
    updateValue(e) {
      this.$emit("input", e);
    },
    fetchData: debounce(function(query) {
      if (query.length < 1) {
        this.data = [];
        return;
      }

      this.$http.post("api/_autocomplete", {
          q: query,
          key: this.requestKey,
          src: this.requestSrc
      }).then(resp => {
        this.data = resp.body;
        this.isFetching = false;
      }, () => {
        console.error("autocomplete api unavailable");
        this.isFetching = false;
      });
    }, 500),
  }
}
</script>

<style>

</style>
