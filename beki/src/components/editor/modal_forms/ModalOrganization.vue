<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="modal-card-title">Organisation</p>
      <button
        type="button"
        class="delete"
        @click="discard"/>
    </header>

    <section class="modal-card-body">
      <div class="block">
      <b-field label="Name:">
        <b-input
            type="text"
            :value="name"
            @input="updateName"
            placeholder="Name"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Straße/Hausnummer:">
        <b-input
            type="text"
            :value="street"
            @input="updateStreet"
            placeholder="Musterstraße 13"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Postleitzahl:">
        <b-input
            type="text"
            :value="zip_code"
            @input="updateZipCode"
            placeholder="12345"
            pattern="[0-9]{5}"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Stadt:">
        <b-input
            type="text"
            :value="city"
            @input="updateCity"
            placeholder="Musterstadt"
            expand
            required>
        </b-input>
      </b-field></div>
      <b-checkbox>TODO: Alle anderen Protokolle aktualisieren?</b-checkbox>
    </section>
    <footer class="modal-card-foot">
        <button class="button is-warning" type="button" @click="discard">Verwerfen</button>
        <button class="button is-primary is-light" @click="commit">Speichern</button>
    </footer>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "ModalOrganization",
  props: {
    commit: Function,
    discard: Function,
  },
  computed: {
    ...mapState({
      id: state => state.tmp.organization.id,
      name: state => state.tmp.organization.name,
      street: state => state.tmp.organization.street,
      zip_code: state => state.tmp.organization.zip_code,
      city: state => state.tmp.organization.city,
    })
  },
  methods: {
    updateName(e) {
      this.$store.commit("tmp/organization/name", e);
    },
    updateStreet(e) {
      this.$store.commit("tmp/organization/street", e);
    },
    updateZipCode(e) {
      this.$store.commit("tmp/organization/zip_code", e);
    },
    updateCity(e) {
      this.$store.commit("tmp/organization/city", e);
    },
  }
}
</script>

<style>

</style>
