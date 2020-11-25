<template>
  <simple-editor-layout title="Prüfkriterium" commit-action="inspectionStandard/store">
    <b-field label="DIN:" horizontal>
      <b-input
        type="text"
        :value="din"
        @input="updateDin"
        placeholder="DIN A4"
        expand
        required>
      </b-input>
    </b-field>
    <b-field label="Versioniert:" horizontal>
      <b-switch
        :value="hasVersion"
        @input="udpateHasVersion"
        true-value="Ja"
        false-value="Nein">
      </b-switch>
    </b-field>
    <b-field label="Beschreibung:" horizontal>
      <b-input
        type="text"
        :value="description"
        @input="updateDescription"
        placeholder="Beschreibung"
        expand
        required>
      </b-input>
    </b-field>
  </simple-editor-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleEditorLayout from '../content/editor/generic/SimpleEditorLayout.vue'

export default {
  components: { SimpleEditorLayout },
  name: "ViewInspectionStandard",
  computed: {
    ...mapGetters('inspectionStandard', [
      'din',
      'description',
      'hasVersion',
    ]),
  },
  methods: {
    updateDin(e) {
      this.$store.commit("inspectionStandard_din", e);
    },
    updateDescription(e) {
      this.$store.commit("inspectionStandard_description", e);
    },
    updateHasVersion(e) {
      this.$store.commit("inspectionStandard_hasVersion", e);
    },
  }
}
</script>

<style>

</style>
