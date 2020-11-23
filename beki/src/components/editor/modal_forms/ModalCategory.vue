<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="modal-card-title">Kategorie</p>
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

      <many-selection-inspection-standard v-model="data.inspection_standards" label="Prüfkriterium aufnehmen:">
      </many-selection-inspection-standard>

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
import ManySelectionInspectionStandard from '../selectors/ManySelectionInspectionStandard.vue';

export default {
  components: { ManySelectionInspectionStandard },
  name: "ModalCategory",
  props: {
    discard: Function,
    commit : Function,
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
            short: "TODO bootstrap category data",
            long: "TODO bootstrap category data"
          },
          is_dirty: true
        }
      },
      tmpInspectionStandard: null
    }
  }
}
</script>

<style>

</style>
