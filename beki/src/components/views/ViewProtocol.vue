<template>
  <div>
  <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="true" :can-cancel="false"></b-loading>
  <div>
    <div class="box" id="protocol-header">
      <status-indicator :status="$store.getters.mainStatus">
        <h4 class="title is-4">Protokoll</h4>
      </status-indicator>

      <editor-protocol-header />
    </div>

    <br>

    <div class="box" v-for="(entry, i) in entries" :id="'entry-' + i" :key="'protocol-entry' + i">
      <status-indicator :status="entry.$status">
        <template slot="default">
          <a class="tag delete is-danger" @click="removeEntry(i)"></a><h5 class="title pl-3 is-5">{{ entry.$repr }}</h5>
        </template>
        <template slot="center">
          <a class="is-light tag" role="button" @click="triggerCollapse(i)">
            <b-icon :icon="entry._collapsed ? 'menu-down' : 'menu-up'" />
          </a>
        </template>
      </status-indicator>
      <hr v-if="entry._collapsed">
      <editor-entry v-show="!entry._collapsed" :index="i" />
    </div>

    <div class="box navigation-sidebar">
      <p><a class="tag is-dark is-medium mt-1" style="width: 100%" href="#protocol-header">
        {{ $store.getters.main.$repr ? $store.getters.main.$repr : 'Protokoll' }}
      </a></p>
      <p v-for="(entry, i) in entries" :key="'entrylink-' + i">
        <a class="tag is-light is-medium mt-1" style="width: 100%" role="button" :href="'#entry-' + i">{{ entry.$repr ? entry.$repr : 'Eintrag ' + (i + 1) }}</a>
      </p>
    </div>

    <div class="field is-grouped is-grouped-centered">
      <p class="control">
        <a class="button is-dark is-outlined" :disabled="isLoading" @click="storeProtocol">
          Speichern
        </a>
      </p>
    </div>
    <br>

    <b-navbar type="is-dark" :fixed-bottom="true" :centered="true">
      <template slot="brand">
      </template>
      <template slot="start">
      </template>

      <template slot="end">
        <b-navbar-item>
        <div class="buttons">
          <a class="button is-light" @click="openPreview" :disabled="isLoading">
              Vorschau
          </a>
        </div>
        </b-navbar-item>
        <b-navbar-item>
        <div class="buttons">
          <a class="button is-light" @click="addEntry" :disabled="isLoading">
              Eintrag hinzufügen
          </a>
        </div>
        </b-navbar-item>
      </template>
    </b-navbar>
  </div>
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
      this.$nextTick(() => {
        window.location.hash = `entry-${this.entries.length - 1}`;
      });
    },
    storeProtocol() {
      if (this.isLoading) {
        return false;
      }

      this.isLoading = true;
      this.$store.dispatch("protocol/store")
        .then(wasUpdated => {
          if (wasUpdated) {
            this.$buefy.snackbar.open("Gespeichert.");
          }
          this.$store.dispatch("back_main", { discard: !wasUpdated });
        }, errors => {
          errors.forEach(err => {
            const idx = err.index === undefined ? '' : ' ' + err.index;
            this.$buefy.snackbar.open({
              duration: 6000,
              message: `${err.target ? err.target : 'Fehler'}${idx}: ${err.msg}`,
              type: 'is-danger',
              queue: false
            })
          })
        })
        .finally(() => this.isLoading = false);
    },
    openPreview() {
      const data = btoa(JSON.stringify(this.$store.getters.main));
      window.open("/api/_render?data=" + data);
    },
    triggerCollapse(index) {
      this.$store.commit("entry_triggerCollapse", { i: index });
    }
  }
}
</script>

<style>
div.navigation-sidebar {
  position: fixed;
  left: 0;
  top: 20%;
  margin-left: 1.5em;
  max-height: 15em;
  max-width: 14em;
  min-width: 14em;
  overflow-y: auto;
}
</style>
