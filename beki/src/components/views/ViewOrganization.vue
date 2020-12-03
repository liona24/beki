<template>
  <simple-editor-layout title="Organisation" commit-action="organization/store">
    <b-field label="Name:" horizontal>
      <b-input
          type="text"
          :value="name"
          @input="updateName"
          placeholder="Name"
          expand
          required>
      </b-input>
    </b-field>
    <b-field label="Straße/Nr.:" horizontal>
      <b-input
          type="text"
          :value="street"
          @input="updateStreet"
          placeholder="Musterstraße 13"
          expand>
      </b-input>
    </b-field>
    <b-field label="Postleitzahl:" horizontal>
      <b-input
          type="text"
          :value="zipCode"
          @input="updateZipCode"
          placeholder="12345"
          pattern="[0-9]{5}"
          expand>
      </b-input>
    </b-field>
    <b-field label="Stadt:" horizontal>
      <b-input
          type="text"
          :value="city"
          @input="updateCity"
          placeholder="Musterstadt"
          expand>
      </b-input>
    </b-field>
  </simple-editor-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleEditorLayout from '../content/editor/generic/SimpleEditorLayout.vue'

export default {
  components: { SimpleEditorLayout },
  name: "ViewOrganization",
  computed: {
    ...mapGetters('organization', [
      'name',
      'street',
      'zipCode',
      'city'
    ]),
  },
  methods: {
    updateName(e) {
      this.$store.commit("organization_name", e);
    },
    updateStreet(e) {
      this.$store.commit("organization_street", e);
    },
    updateZipCode(e) {
      this.$store.commit("organization_zipCode", e);
    },
    updateCity(e) {
      this.$store.commit("organization_city", e);
    },
  }
}
</script>

<style>

</style>
