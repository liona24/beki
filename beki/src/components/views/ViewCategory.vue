<template>
  <simple-editor-layout title="Kategorie" commit-action="category/store">
    <b-field label="Name:" horizontal>
      <b-input
          type="text"
          :value="name"
          @input="updateName"
          expand
          required>
      </b-input>
    </b-field>
    <autocomplete-many-select
      request-src="inspection_standard"
      label="Prüfkriterien:"
      :value="inspectionStandards"
      :create="createInspectionStandard"
      update="category_updateInspectionStandard"
      remove="category_removeInspectionStandard">
    </autocomplete-many-select>
  </simple-editor-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleEditorLayout from '../content/editor/generic/SimpleEditorLayout.vue'
import AutocompleteManySelect from '../utility/AutocompleteManySelect'
import { inspectionStandardState } from '../../store/inspection_standard'

export default {
  components: { SimpleEditorLayout, AutocompleteManySelect },
  name: "ViewCategory",
  computed: {
    ...mapGetters('category', [
        'name',
        'inspectionStandards',
      ]),
  },
  methods: {
    updateName(e) {
      this.$store.commit("category_name", e);
    },
    createInspectionStandard() {
      const obj = inspectionStandardState();
      return obj;
    }
  }
}
</script>

<style>

</style>
