<template>
  <div>
    <div>
      <b-field grouped positition="is-right">
        <autocomplete-select
          label="Kategorie:"
          endpoint="api/category"

          update="entry_category"
          :update-args="{ i: index }"

          :value="category"
          @input="updateCategory">
        </autocomplete-select>

        <b-field label="Version:" horizontal position="is-right">
          <b-input :value="categoryVersion" @input="updateCategoryVersion" type="number" :maxlength="4" required></b-input>
        </b-field>
      </b-field>
    </div>
    <hr>

    <section>
    <autocomplete-text :default="title" @update:value="updateTitle" required>
      Bezeichnung (entries:title):
    </autocomplete-text>

    <autocomplete-text :default="manufacturer" @update:value="updateManufacturer" required>
      Hersteller (entries:manufacturer):
    </autocomplete-text>

    <b-field label="Baujahr:" horizontal>
      <b-input type="number" :maxlength="4" placeholder="Baujahr" :value="yearBuilt" @input="updateYearBuilt"></b-input>
    </b-field>

    <autocomplete-text :default="inspectionSigns" @update:value="updateInspectionSigns" required>
      Prüfzeichen (entries:inspection_signs):
    </autocomplete-text>

    <b-field label="Herstellerinformation:" horizontal>
      <b-field>
        <b-radio-button expanded :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
          native-value="Ja"
          type="is-success is-light">
          <b-icon icon="check"></b-icon>
          <span>Ja</span>
        </b-radio-button>

        <b-radio-button expanded :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
          native-value="Nein"
          type="is-danger is-light">
          <b-icon icon="close"></b-icon>
          <span>Nein</span>
        </b-radio-button>

        <b-radio-button expanded :value="manufactureInfoAvailable" @input="updateManufactureInfoAvailable"
          native-value="Keine Angabe"
          type="is-dark">
          <span>Keine Angabe</span>
        </b-radio-button>
      </b-field>
    </b-field>

    <b-field label="Leicht zugänglich:" horizontal>
      <b-field>
        <b-radio-button expanded :value="easyAccess" @input="updateEasyAccess"
          native-value="Ja"
          type="is-success is-light">
          <b-icon icon="check"></b-icon>
          <span>Ja</span>
        </b-radio-button>

        <b-radio-button expanded :value="easyAccess" @input="updateEasyAccess"
          native-value="Nein"
          type="is-danger is-light">
          <b-icon icon="close"></b-icon>
          <span>Nein</span>
        </b-radio-button>

        <b-radio-button expanded :value="easyAccess" @input="updateEasyAccess"
          native-value="Keine Angabe"
          type="is-dark">
          <span>Keine Angabe</span>
        </b-radio-button>
      </b-field>
    </b-field>
    </section>

    <br>
    <editor-flaw v-for="(_flaw, i) in flaws" :entry="index" :index="i" :key="i" />

    <b-button size="is-small" type="is-dark" outlined expanded @click="addFlaw">
      <b-icon icon="chevron-double-right" size="is-small"></b-icon> Mangel hinzufügen
    </b-button>
  </div>
</template>

<script>
import EditorFlaw from './EditorFlaw.vue'
import AutocompleteText from '../../utility/AutocompleteText.vue'
import AutocompleteSelect from '../../utility/AutocompleteSelect.vue'

import { mapGetters } from 'vuex';

export default {
  components: { EditorFlaw, AutocompleteText, AutocompleteSelect },
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
    addFlaw() {
      console.log("Add flaw", this.index, this.entries);
      this.$store.commit("entry_addFlaw", { i: this.index });
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
