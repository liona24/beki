<template>
  <div class="block">
    <b-field horizontal :type="isValid ? '' : 'is-danger'" :message="message">
      <b-autocomplete
        v-model="innerValue"
        :data="filteredDataArray"
        placeholder="..."
        clearable
        :required="required"
        @select="option => innerValue = option">
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
export default {
  name: "AutocompleteInput",
  props: {
    name: String,
    validator: {
      type: Function,
      default: () => null,
    },
    required: {
      type: Boolean,
      default: false
    },
    default: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      message: null,
      innerValue: this.default,
      filteredDataArray: ["Hi", "Bye"]
    }
  },
  computed: {
    isValid() {
      return this.message === null || this.message.length === 0;
    }
  },
  watch: {
    innerValue() {
      this.message = this.validator(this.innerValue);

      if (this.isValid) {
        this.$emit("update:value", this.innerValue);
      } else {
        this.$emit("update:value", null);
      }
    }
  },
  methods: {
    fetchData() {
      // TODO: fetch actual data
    },
  }
}
</script>

<style>

</style>
