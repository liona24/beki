<template>
  <div>
    <div class="content columns">
      <div class="column">
        <autocomplete-select
          label="Kategorie:"
          endpoint="api/category"
          :value="category"
          @input="updateCategory">
        </autocomplete-select>
      </div>

      <div class="column is-one-quarter">
        <b-field label="Version:" horizontal>
          <b-input :value="categoryVersion" @input="updateCategoryVersion" expanded type="number" :maxlength="4" required></b-input>
        </b-field>
      </div>
    </div>
    <div class="sep-line-small"><hr></div>

    <autocomplete-text :default="title" @update:value="updateTitle" required>
      Bezeichnung (entries:title):
    </autocomplete-text>

    <autocomplete-text :default="manufacturer" @update:value="updateManufacturer" required>
      Hersteller (entries:manufacturer):
    </autocomplete-text>

    <b-field label="Baujahr:" horizontal>
      <b-input type="number" :maxlength="4" placeholder="Baujahr" :value="yearBuilt" @input="udpateYearBuilt"></b-input>
    </b-field>

    <autocomplete-text :default="inspectionSigns" @update:value="updateInspectionSigns" required>
      Prüfzeichen (entries:inspection_signs):
    </autocomplete-text>

    <b-field label="Herstellerinformation:" horizontal>
      <b-radio-button :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
        native-value="Ja"
        type="is-success is-light">
        <b-icon icon="check"></b-icon>
        <span>Ja</span>
      </b-radio-button>

      <b-radio-button :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
        native-value="Nein"
        type="is-danger is-light">
        <b-icon icon="close"></b-icon>
        <span>Nein</span>
      </b-radio-button>

      <b-radio-button :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
        native-value="Keine Angabe"
        type="is-primary is-light">
        <span>Keine Angabe</span>
      </b-radio-button>
    </b-field>

    <b-field label="Leicht zugänglich:" horizontal>
      <b-radio-button :value="easyAccess" @input="updateEasyAccess"
        native-value="Ja"
        type="is-success is-light">
        <b-icon icon="check"></b-icon>
        <span>Ja</span>
      </b-radio-button>

      <b-radio-button :value="easyAccess" @input="updateEasyAccess"
        native-value="Nein"
        type="is-danger is-light">
        <b-icon icon="close"></b-icon>
        <span>Nein</span>
      </b-radio-button>

      <b-radio-button :value="easyAccess" @input="updateEasyAccess"
        native-value="Keine Angabe"
        type="is-primary is-light">
        <span>Keine Angabe</span>
      </b-radio-button>
    </b-field>

    <editor-flaw v-for="(_flaw, i) in flaws" :entry="index" :index="i" :key="i" />

    <b-button size="is-small" type="is-primary" outlined expanded>
      <b-icon icon="chevron-double-right" size="is-small"></b-icon> Mangel hinzufügen
    </b-button>
  </div>
</template>

<script>
import EditorFlaw from './EditorFlaw.vue'
// import SelectionCategory from './selectors/SelectionCategory.vue'
import AutocompleteText from '../../utility/AutocompleteText.vue'
import { mapGetters } from 'vuex';

export default {
  components: { EditorFlaw, AutocompleteText },
  name: "EditorEntry",
  props: {
    index: Number,
  },
  computed: {
    ...mapGetters('protocol', ['entries']),
    title() {
      return this.entries[this.index].title;
    },
    category() {
      return this.entries[this.index].category;
    },
    categoryVersion() {
      return this.entries[this.index].category_version;
    },
    manufacturer() {
      return this.entries[this.index].manufacturer;
    },
    manufactureInfoAvailable() {
      return this.entries[this.index].manufacture_info_available;
    },
    yearBuilt() {
      return this.entries[this.index].year_built;
    },
    inspectionSigns() {
      return this.entries[this.index].inspection_signs;
    },
    easyAccess() {
      return this.entries[this.index].easy_access;
    },
    flaws() {
      return this.entries[this.index].flaws;
    }
  },
  methods: {
    updateCategory(e) {
      this.$store.commit("entry_category", { i: this.index, val: e });
    },
    updateCategoryVersion(e) {
      this.$store.commit("entry_categoryVersion", { i: this.index, val: e });
    },
    updateTitle(e) {
      this.$store.commit("entry_title", { i: this.index, val: e });
    },
    updateManufacturer(e) {
      this.$store.commit("entry_manufacturer", { i: this.index, val: e });
    },
    updateYearBuilt(e) {
      this.$store.commit("entry_yearBuilt", { i: this.index, val: e });
    },
    updateInspectionSigns(e) {
      this.$store.commit("entry_inspectionSigns", { i: this.index, val: e });
    },
    updateManufactureInfoAvailable(e) {
      this.$store.commit("entry_manufactureInfoAvailable", { i: this.index, val: e });
    },
    updateEasyAccess(e) {
      this.$store.commit("entry_easyAccess", { i: this.index, val: e });
    },
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
