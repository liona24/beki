<template>
  <simple-editor-layout title="Einrichtung" commit-action="facility/store">
    <p> TODO: Bild einfügen </p>
    <b-field label="Name:" horizontal>
      <b-input
          type="text"
          :value="name"
          @input="updateName"
          placeholder="Kindergarten Musterstadt"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="Straße/Hausnr:" horizontal>
      <b-input
          type="text"
          :value="street"
          @input="updateStreet"
          placeholder="Musterstraße 13"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="Postleitzahl:" horizontal>
      <b-input
          type="text"
          :value="zipCode"
          @input="updateZipCode"
          placeholder="12345"
          pattern="[0-9]{5}"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="Stadt:" horizontal>
      <b-input
          type="text"
          :value="city"
          @input="updateCity"
          placeholder="Musterstadt"
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
  name: "ViewFacility",
  computed: {
    ...mapGetters('facility', [
      'name',
      'street',
      'zipCode',
      'city',
    ]),
  },
  methods: {
    updateName(e) {
      this.$store.commit("facility_name", e);
    },
    updateStreet(e) {
      this.$store.commit("facility_street", e);
    },
    updateZipCode(e) {
      this.$store.commit("facility_zipCode", e);
    },
    updateCity(e) {
      this.$store.commit("facility_city", e);
    },
  }
}
</script>

<style>

</style>
