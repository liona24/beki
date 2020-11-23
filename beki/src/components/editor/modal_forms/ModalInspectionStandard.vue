<template>
  <div class="modal-card" style="width: auto">
    <header class="modal-card-head">
      <p class="modal-card-title">Prüfkriterium</p>
      <button
        type="button"
        class="delete"
        @click="discard(initial)"/>
    </header>

    <section class="modal-card-body">
      <div class="block">
        <b-field label="DIN:">
          <b-input
              type="text"
              v-model="data.din"
              placeholder="DIN A4"
              expand
              required>
          </b-input>
        </b-field></div>
      <div class="block">
        <b-field label="Versioniert:">
          <b-switch v-model="data.has_version"
            true-value="Ja"
            false-value="Nein">
          </b-switch>
        </b-field>
      </div>
      <div class="block">
      <b-field label="Beschreibung:">
        <b-input
            type="text"
            v-model="data.description"
            placeholder="Beschreibung"
            expand
            required>
        </b-input>
      </b-field></div>
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
  name: "ModalInspectionStandard",
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
            short: "TODO bootstrap inspection standard data",
            long: "TODO bootstrap inspection standard data"
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
