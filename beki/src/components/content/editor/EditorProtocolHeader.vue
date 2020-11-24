<template>
  <section class="section">
    <autocomplete-text
      :default="title"
      @update:value="updateTitle"
      required>
      Titel:
    </autocomplete-text>

    <b-field label="Prüfgrundlagen (overview):" horizontal>
      <textarea class="textarea"
        :value="overview"
        @input="updateOverview">
        TODO: Add autocomplete
      </textarea>
    </b-field>

    <autocomplete-select
      endpoint="api/facility"
      label="Objekt:"
      :value="facility"
      @input="updateFacility">
    </autocomplete-select>

    <b-field label="Prüfdatum:" horizontal>
      <b-input :value="inspectionDate"
        @input="updateInspectionDate"
        expanded
        type="date"
        required>
      </b-input>
    </b-field>

    <autocomplete-select
      endpoint="api/inspector"
      label="Prüfer:"
      :value="inspector"
      @input="updateInspector">
    </autocomplete-select>

    <autocomplete-select
      endpoint="api/organization"
      label="Auftraggeber:"
      :value="issuer"
      @input="updateIssuer">
    </autocomplete-select>

    <b-field label="Weitere Teilnehmer:" horizontal>
      <b-input
        :value="attendees"
        @input="updateAttendees"
        expanded
        type="text">
      </b-input>
    </b-field>
  </section>

</template>

<script>
import AutocompleteText from '../../utility/AutocompleteText'
import AutocompleteSelect from '../../utility/AutocompleteSelect.vue'

import { mapGetters } from 'vuex'

export default {
  components: { AutocompleteText, AutocompleteSelect },
  name: "EditorProtocolHeader",
  computed: {
    ...mapGetters('protocol', [
      'title',
      'overview',
      'attendees',
      'inspectionDate',
      'facility',
      'inspector',
      'issuer'
    ])
  },
  methods: {
    updateTitle(e) {
      this.$store.commit("protocol_title", e);
    },
    updateOverview(e) {
      console.log("TODO: fix textarea", e.target.value);
      this.$store.commit("protocol_overview", e.target.value);
    },
    updateAttendees(e) {
      this.$store.commit("protocol_attendees", e);
    },
    updateInspectionDate(e) {
      this.$store.commit("protocol_inspectionDate", e);
    },
    updateFacility(e) {
      this.$store.commit("protocol_facility", e);
    },
    updateInspector(e) {
      this.$store.commit("protocol_inspector", e);
    },
    updateIssuer(e) {
      this.$store.commit("protocol_issuer", e);
    },
  }
}
</script>

<style>

</style>
