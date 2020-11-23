<template>
  <div>
    <div class="content columns">
      <div class="column">
        <selection-category v-model="category"></selection-category>
      </div>

      <div class="column is-one-quarter">
        <b-field label="Version:" horizontal>
          <b-input v-model="category_version" expanded type="number" :maxlength="4" required></b-input>
        </b-field>
      </div>
    </div>
    <div class="sep-line-small"><hr></div>

    <autocomplete-input :default="title" @update:value="title = $event" required>
      Bezeichnung (entries:title):
    </autocomplete-input>

    <autocomplete-input :default="manufacturer" @update:value="manufacturer = $event" required>
      Hersteller (entries:manufacturer):
    </autocomplete-input>

    <b-field label="Baujahr:" horizontal>
      <b-input type="number" :maxlength="4" placeholder="Baujahr" v-model="year_built"></b-input>
    </b-field>

    <autocomplete-input :default="inspection_signs" @update:value="inspection_signs = $event" required>
      Prüfzeichen (entries:inspection_signs):
    </autocomplete-input>

    <b-field label="Herstellerinformation:" horizontal>
      <b-radio-button v-model="manufacture_info_available"
        native-value="Ja"
        type="is-success is-light">
        <b-icon icon="check"></b-icon>
        <span>Ja</span>
      </b-radio-button>

      <b-radio-button v-model="manufacture_info_available"
        native-value="Nein"
        type="is-danger is-light">
        <b-icon icon="close"></b-icon>
        <span>Nein</span>
      </b-radio-button>

      <b-radio-button v-model="manufacture_info_available"
        native-value="Keine Angabe"
        type="is-primary is-light">
        <span>Keine Angabe</span>
      </b-radio-button>
    </b-field>

    <b-field label="Leicht zugänglich:" horizontal>
      <b-radio-button v-model="easy_access"
        native-value="Ja"
        type="is-success is-light">
        <b-icon icon="check"></b-icon>
        <span>Ja</span>
      </b-radio-button>

      <b-radio-button v-model="easy_access"
        native-value="Nein"
        type="is-danger is-light">
        <b-icon icon="close"></b-icon>
        <span>Nein</span>
      </b-radio-button>

      <b-radio-button v-model="easy_access"
        native-value="Keine Angabe"
        type="is-primary is-light">
        <span>Keine Angabe</span>
      </b-radio-button>
    </b-field>

    <editor-flaw />

    <b-button size="is-small" type="is-primary" outlined expanded>
      <b-icon icon="chevron-double-right" size="is-small"></b-icon> Mangel hinzufügen
    </b-button>
  </div>
</template>

<script>
import EditorFlaw from './EditorFlaw.vue'
import SelectionCategory from './selectors/SelectionCategory.vue'
import AutocompleteInput from '../utility/AutocompleteInput.vue'

export default {
  components: { EditorFlaw, SelectionCategory, AutocompleteInput },
  name: "EditorEntry",
  data() {
    return {
      category: null,
      category_version: 0,
      title: "",
      manufacturer: "",
      year_built: 0,
      inspection_signs: "",
      manufacture_info_available: "Keine Angabe",
      easy_access: "Keine Angabe",
    }

  }
}
</script>

<style>

.sep-line-small hr {
  height: 2px;
  background-color: #595fe1;
  margin-left: 25px;
  margin-right: 25px;
}

</style>
