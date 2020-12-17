<template>
  <div>
  <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="true" :can-cancel="false"></b-loading>
  <div class="box">
    <b-steps v-model="activeStep"
      :animated="true"
      :rounded="true"
      :has-navigation="false"
      label-position="bottom">
      <b-step-item step="1" label="Einrichtung auswählen" :clickable="false">
        <section>
          <br>
          <autocomplete-select
            request-src="facility"
            label="Objekt:"
            :value="facility"
            update="wizard_facility">
          </autocomplete-select>
          <br>

          <div class="field is-grouped is-grouped-right">
            <button class="button is-dark is-outlined" :disabled="isLoading || !facility || facility.id === null" @click="prepare">Weiter</button>
          </div>
        </section>
      </b-step-item>

      <b-step-item step="2" label="Anordnen" :clickable="false">

        <draggable v-model="protocolSkeleton"
          tag="div"
          :group="{ name: 'g1' }"
          @start="isDragging = true"
          @end="isDragging = false">
          <div v-for="entry in protocolSkeleton" :key="entry.index" class="box" style="overflow-x: auto">
            <b-field>
              <b-input v-model="entry.title" placeholder="Neuer Eintrag" type="text"></b-input>
            </b-field>
            <draggable v-model="entry.flaws"
              tag="div"
              class="tile is-ancestor"
              :group="{ name: 'g2' }"
              @start="isDragging = true"
              @end="isDragging = false">

              <div class="tile is-parent" v-for="flaw in entry.flaws" :key="flaw.ident">
                <div class="tile is-child" style="display: flex; justify-content: center">
                  <figure class="image is-128x128" >
                    <img :src="'/images/' + flaw.img" class="is-rounded" style="border-radius: .3em" />
                  </figure>
                </div>
              </div>
            </draggable>

            <br>

          </div>
        </draggable>

        <br>
        <div class="field is-grouped is-grouped-right">
          <b-button type="is-dark" outlined :disabled="isLoading" @click="finish">Weiter</b-button>
        </div>
      </b-step-item>
    </b-steps>
  </div>
  </div>
</template>

<script>
import AutocompleteSelect from '../utility/AutocompleteSelect'
import draggable from 'vuedraggable'
import { flawState } from '../../store/flaw'
import { protocolState } from '../../store/protocol'
import { entryState } from '../../store/entry'

import { mapGetters } from 'vuex'
import { SyncStatus } from '../../store/common'

export default {
  components: { AutocompleteSelect, draggable },
  name: "ViewWizard",
  data() {
    return {
      isDragging: false,
      isLoading: false,
      activeStep: 0,
      protocolSkeleton: []
    }
  },
  computed: {
    ...mapGetters('wizard', ['facility', 'images', 'isPreprocessingWorking'])
  },
  watch: {
    isDragging() {
      if (this.isDragging) {
        return;
      }

      const filtered = this.protocolSkeleton
        .filter(entry => entry.flaws.length > 0)
        .map((entry, i) => {
          entry.index = i;
          return entry;
        });
      filtered.push({
        id: null,
        index: filtered.length,
        title: '',
        flaws: []
      });
      this.protocolSkeleton = filtered;
    }
  },
  methods: {
    prepare() {
      if (this.facility?.id === null) {
        return;
      }

      const fetchTitle = (id, fallback) => {
        return new Promise(resolve => {
          fetch(`/api/entry/${id}`)
          .then(resp => resp.json())
          .then(json => {
            resolve(json.title);
          })
          .catch(() => {
            resolve(fallback);
          });
        });
      }

      this.isLoading = true;
      const cont = () => {
        const body = {
          images: this.images,
          facility: this.facility.id,
        };
        fetch("/api/_wizard/autocompose", {
          method: "POST",
          body: JSON.stringify(body),
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(resp => resp.json())
        .then(json => {
          let glob_flaw_ident = 1;
          const entries = json.map((v, i) => {
            const entry = {
              id: v.id,
              index: i,
              title: '',
              flaws: v.flaws.map(f => {
                return {
                  ident: 'flaw-' + glob_flaw_ident++,
                  img: f,
                };
              })
            };

            if (entry.id !== null) {
              fetchTitle(entry.id, `Eintrag ${i + 1}`)
              .then(title => {
                if (!entry.title) {
                  entry.title = title;
                }
              });
            }

            return entry;
          });

          entries.push({
            id: null,
            index: entries.length,
            title: '',
            flaws: []
          });

          this.protocolSkeleton = entries;
          this.activeStep = 1;
        })
        .catch(() => {
          this.showError("Da ist etwas schiefgelaufen. Versuche es nochmal");
        })
        .finally(() => {
          this.isLoading = false;
        })
      };

      const poll = setInterval(() => {
        if (!this.isPreprocessingWorking) {
          clearInterval(poll);
          cont();
        }
      }, 300);
    },
    finish() {
      if (this.isLoading) {
        return;
      }

      this.isLoading = true;
      const entries = this.protocolSkeleton
        .filter(entry => entry.flaws.length > 0)
        .map(entry => {
          const flaws = entry.flaws.map(f => f.img);
          return {
            id: entry.id,
            title: entry.title,
            flaws: flaws
          }
        });

      fetch("/api/_wizard/assemble", {
        method: "POST",
        body: JSON.stringify({ entries: entries, facility: this.facility.id }),
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(resp => resp.json())
      .then(json => {
        const protocol = Object.assign(protocolState(), json);
        protocol.$status |= SyncStatus.New | SyncStatus.Modified;
        protocol.$repr = protocol.title;

        protocol.entries = protocol.entries.map(e => {
          const entry = Object.assign(entryState(), e);
          entry.$status |= SyncStatus.New | SyncStatus.Modified;
          entry.$repr = entry.title;

          entry.flaws = entry.flaws.map(f => {
            const flaw = Object.assign(flawState(), f);
            flaw.$status |= SyncStatus.New | SyncStatus.Modified;
            flaw.$repr = flaw.title;
            return flaw;
          });

          return entry;
        });

        this.$store.dispatch("back_main", { discard: false }).then(() => {
          this.$store.commit('push_main', { view: protocol, callback: "menu_currentPreviewId", args: null }, { root: true });
        });
      })
      .catch(e => {
        console.error("wizard finish", e);
        this.showError("Fehler: Bitte erneut versuchen!");
      })
      .finally(() => this.isLoading = false);
    },
    showError(msg) {
      this.$buefy.snackbar.open({
        duration: 6000,
        message: msg,
        type: 'is-danger',
        queue: false
      });
    }
  }
}
</script>

<style>
</style>
