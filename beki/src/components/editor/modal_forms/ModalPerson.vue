<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="modal-card-title">Person</p>
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
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="Vorname:">
        <b-input
            type="text"
            v-model="data.first_name"
            expand
            required>
        </b-input>
      </b-field></div>
      <div class="block">
      <b-field label="E-Mail:">
        <b-input
            type="email"
            v-model="data.email"
            expand>
        </b-input>
      </b-field></div>
      <selection-organization v-model="data.organization"></selection-organization>
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
import SelectionOrganization from '../selectors/SelectionOrganization.vue';

export default {
  components: { SelectionOrganization },
  name: "ModalPerson",
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
            short: "TODO bootstrap person data",
            long: "TODO bootstrap person data"
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
