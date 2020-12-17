<template>
  <b-field :horizontal="!noLabel">
    <b-autocomplete
      :value="value"
      @input="updateValue"

      :data="data"
      :loading="isFetching"
      @typing="fetchData"

      :placeholder="placeholder"
      clearable
      :required="required"
      @select="updateValue">
      <template slot="empty">Keine Übereinstimmung</template>
    </b-autocomplete>
    <template v-if="!noLabel" slot="label">
      <slot>
      </slot>
    </template>
  </b-field>
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
    placeholder: {
      type: String,
      default: "..."
    },
    noLabel: {
      type: Boolean,
      default: false,
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
