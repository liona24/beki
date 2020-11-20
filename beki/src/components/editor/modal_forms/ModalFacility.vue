<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="modal-card-title">Objekt/Einrichtung</p>
      <button
        type="button"
        class="delete"
        @click="discard(initial)"/>
    </header>

    <section class="modal-card-body">
      <div class="block">
      <b-field label="Name:">
        <b-input
            type="text"
            v-model="data.name"
            placeholder="Kindergarten Musterstadt"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Straße/Hausnummer:">
        <b-input
            type="text"
            v-model="data.street"
            placeholder="Musterstraße 13"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Postleitzahl:">
        <b-input
            type="text"
            v-model="data.zip_code"
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
            v-model="data.city"
            placeholder="Musterstadt"
            expand
            required>
        </b-input>
      </b-field></div>
      <b-checkbox>TODO: Alle anderen Protokolle aktualisieren?</b-checkbox>
    </section>
    <footer class="modal-card-foot">
        <button class="button is-warning" type="button" @click="discard(initial)">Verwerfen</button>
        <button class="button is-primary is-light" @click="() => commit(data)">Speichern</button>
    </footer>
  </div>
</template>

<script>
import cloneDeep from 'lodash.clonedeep';

export default {
  name: "ModalFacility",
  props: {
    discard: Function,
    commit: Function,
    initial: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      data: this.initial ? cloneDeep(this.initial) : {
        id: null,
        meta: {
          repr: {
            short: "TODO bootstrap facility data",
            long: "TODO bootstrap facility data"
          },
          is_dirty: true
        }
      }
    }
  }
}
</script>

<style>

</style>
