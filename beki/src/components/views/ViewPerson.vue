<template>
  <simple-editor-layout title="Person" commit-action="person/store">
    <b-field label="Name:" horizontal>
      <b-input
          type="text"
          :value="name"
          @input="updateName"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="Vorname:" horizontal>
      <b-input
          type="text"
          :value="firstName"
          @input="updateFirstName"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="E-Mail:" horizontal>
      <b-input
          type="email"
          :value="email"
          @input="updateEmail"
          expand>
      </b-input>
    </b-field>
    <autocomplete-select
      endpoint="api/organization"
      label="Organisation:"
      :value="organization"
      update="person_organization">
    </autocomplete-select>
  </simple-editor-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleEditorLayout from '../content/editor/generic/SimpleEditorLayout.vue'
import AutocompleteSelect from '../utility/AutocompleteSelect'

export default {
  components: { SimpleEditorLayout, AutocompleteSelect },
  name: "ViewPerson",
  computed: {
    ...mapGetters('person', [
      'name',
      'firstName',
      'email',
      'organization'
    ]),
  },
  methods: {
    updateName(e) {
      this.$store.commit("person_name", e);
    },
    updateFirstName(e) {
      this.$store.commit("person_firstName", e);
    },
    updateEmail(e) {
      this.$store.commit("person_email", e);
    },
  }
}
</script>

<style>

</style>
