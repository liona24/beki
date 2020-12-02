<template>
  <div>
    <autocomplete-text
      :value="title"
      @input="updateTitle"
      request-key="title"
      request-src="protocol"
      required>
      Titel:
    </autocomplete-text>

    <b-field label="Prüfgrundlagen:" horizontal>
      <textarea class="textarea"
        :value="overview"
        @input="updateOverview">
      </textarea>
    </b-field>

    <autocomplete-select
      request-src="facility"
      label="Objekt:"
      :value="facility"
      update="protocol_facility">
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
      request-src="person"
      label="Prüfer:"
      :value="inspector"
      update="protocol_inspector">
    </autocomplete-select>

    <autocomplete-select
      request-src="organization"
      label="Auftraggeber:"
      :value="issuer"
      update="protocol_issuer">
    </autocomplete-select>

    <b-field label="Weitere Teilnehmer:" horizontal>
      <b-input
        :value="attendees"
        @input="updateAttendees"
        expanded
        type="text">
      </b-input>
    </b-field>
  </div>
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
