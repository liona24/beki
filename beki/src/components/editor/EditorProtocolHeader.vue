<template>
  <div>
    <autocomplete-input :default="title" @update:value="title = $event" required>
      Titel:
    </autocomplete-input>

    <b-field label="Prüfgrundlagen (overview):" horizontal>
      <textarea class="textarea">
        TODO: Add autocomplete
      </textarea>
    </b-field>

    <selection-facility v-model="facility" />

    <b-field label="Prüfdatum:" horizontal>
      <b-input v-model="inspectionDate" expanded type="date" required></b-input>
    </b-field>

    <cross-reference-selection label="Prüfer (inspector):" required>
    </cross-reference-selection>

    <cross-reference-selection label="Auftraggeber (issuer):" required>
    </cross-reference-selection>

    <b-field label="Weitere Teilnehmer:" horizontal>
      <b-input v-model="attendees" expanded type="text"></b-input>
    </b-field>
  </div>

</template>

<script>
import AutocompleteInput from '../utility/AutocompleteInput.vue'
import CrossReferenceSelection from '../utility/CrossReferenceSelection.vue'
import SelectionFacility from './selectors/SelectionFacility.vue'

export default {
  components: { AutocompleteInput, CrossReferenceSelection, SelectionFacility },
  name: "EditorProtocolHeader",
  data() {
    return {
      title: "Hi",
      attendees: "",
      inspectionDate: "",

      facility: null,
    }
  },
  methods: {
  }
}
</script>

<style>

</style>
