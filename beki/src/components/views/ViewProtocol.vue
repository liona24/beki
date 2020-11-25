<template>
  <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="true" :can-cancel="false"></b-loading>
  <div v-else>
    <status-indicator :status="$store.getters.currentStatus">
      <h4 class="title is-4">Protokoll</h4>
    </status-indicator>

    <editor-protocol-header />

    <br>
    <br>

    <div class="box" v-for="(entry, i) in entries" :key="i">
      <status-indicator :status="entry.$status">
        <a class="tag delete is-danger" @click="removeEntry(i)"></a> {{ entry.$repr }}
      </status-indicator>
      <editor-entry :index="i" />
    </div>

    <div class="field is-grouped is-grouped-centered">
      <p class="control">
        <a class="button is-dark is-outlined" @click="addEntry">
          Eintrag hinzufügen
        </a>
      </p>
    </div>

    <b-navbar type="is-dark" :fixed-bottom="true" :centered="true">
      <template slot="brand">
      </template>
      <template slot="start">
        <div class="buttons">
          <a class="button is-light" @click="storeProtocol">
              Speichern
          </a>
        </div>
      </template>

      <template slot="end">
      </template>
    </b-navbar>
  </div>
</template>

<script>
import EditorProtocolHeader from '../content/editor/EditorProtocolHeader.vue'
import EditorEntry from '../content/editor/EditorEntry.vue'
import StatusIndicator from '../utility/StatusIndicator'
import { mapGetters } from 'vuex'

export default {
  components: { EditorProtocolHeader, EditorEntry, StatusIndicator },
  name: "Editor",
  data() {
    return {
      isLoading: false,
    }
  },
  computed: {
    ...mapGetters('protocol', ['entries'])
  },
  methods: {
    removeEntry(i) {
      this.$store.commit("protocol_removeEntry", i);
    },
    addEntry() {
      this.$store.commit("protocol_addEntry");
    },
    storeProtocol() {
      console.log("TODO store protocol");
    }
  }

}
</script>

<style>

</style>
