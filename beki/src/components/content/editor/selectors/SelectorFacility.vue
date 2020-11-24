<template>
  <autocomplete-select
    :label="label"
    :value="value"
    @input="updateValue"
    @edit="edit"
    @new="createNew"
    required>
  </autocomplete-select>
</template>

<script>
import AutocompleteSelect from '../../../utility/AutocompleteSelect.vue'
import { facilityState } from '../../../../store/facility'

export default {
  name: "SelectionFacility",
  components: { AutocompleteSelect },
  props: {
    value: Object,
    label: {
      type: String,
      default: "Objekt:"
    }
  },
  methods: {
    edit() {

      this.$store.commit("push", )
      this.isModalVisible = true;
    },
    createNew() {
      this.isModalVisible = false;

      if(selectedObj !== null) {
        this.bubbleInput(selectedObj);
      }
    },
    updateValue(obj) {
      this.$emit("input", obj);
    }
  }
}
</script>

<style>

</style>
