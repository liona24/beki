<template>
  <div>
    <autocomplete-input
      :default="title"
      @update:value="updateTitle"
      required>
      Titel:
    </autocomplete-input>

    <b-field label="Prüfgrundlagen (overview):" horizontal>
      <textarea class="textarea"
        :value="overview"
        @input="updateOverview">
        TODO: Add autocomplete
      </textarea>
    </b-field>

    <selection-facility
      :value="facility"
      @input="updateFacility">
    </selection-facility>

    <b-field label="Prüfdatum:" horizontal>
      <b-input :value="inspection_date"
        @input="updateInspectionDate"
        expanded
        type="date"
        required>
      </b-input>
    </b-field>

    <selection-person
      :value="inspector"
      @input="updateInspector"
      label="Prüfer:">
    </selection-person>

    <selection-organization
      :value="issuer"
      @input="updateIssuer"
      label="Auftraggeber:">
    </selection-organization>

    <b-field label="Weitere Teilnehmer:" horizontal>
      <b-input
        :value="attendees"
        @input="updateAttendees"
        expanded
        type="text">
      </b-input>
    </b-field>

    <p>{{ $store.state.protocol.value }}</p>
  </div>

</template>

<script>
import AutocompleteInput from '../utility/AutocompleteInput.vue'
import SelectionFacility from './selectors/SelectionFacility.vue'
import SelectionOrganization from './selectors/SelectionOrganization.vue'
import SelectionPerson from './selectors/SelectionPerson.vue'

import { mapState } from 'vuex'

export default {
  components: { AutocompleteInput, SelectionFacility, SelectionOrganization, SelectionPerson },
  name: "EditorProtocolHeader",
  computed: {
    ...mapState({
      title: state => state.protocol.title,
      overview: state => state.protocol.overview,
      attendees: state => state.protocol.attendees,
      inspection_date: state => state.protocol.inspection_date,

      facility: state => state.protocol.facility,
      inspector: state => state.protocol.inspector,
      issuer: state => state.protocol.issuer
    })
  },
  methods: {
    updateTitle(e) {
      this.$store.commit("protocol/title", e);
    },
    updateOverview(e) {
      console.log(e.target.value);
      this.$store.commit("protocol/overview", e.target.value);
    },
    updateAttendees(e) {
      this.$store.commit("protocol/attendees", e);
    },
    updateInspectionDate(e) {
      this.$store.commit("protocol/inspection_date", e);
    },
    updateFacility(e) {
      this.$store.commit("protocol/facility", e);
    },
    updateInspector(e) {
      this.$store.commit("protocol/inspector", e);
    },
    updateIssuer(e) {
      this.$store.commit("protocol/issuer", e);
    },
  }
}
</script>

<style>

</style>
