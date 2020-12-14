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
        <autocomplete-select
          request-src="facility"
          label="Objekt:"
          :value="facility"
          update="wizard_facility">
        </autocomplete-select>
        <b-field position="is-right">
          <b-button type="is-dark" outlined :disabled="isLoading || facility.id === null" @click="prepare">Weiter</b-button>
        </b-field>
      </b-step-item>

      <b-step-item step="2" label="Bilder anordnen" :clickable="false">

        <draggable :list="protocolSkeleton">
          <div v-for="(entry, i) in protocolSkeleton" :key="'wpe' + i" class="box">
            <h1>{{ entry }}</h1>
            <draggable :list="entry.flaws">
              <div v-for="(flaw_img, j) in entry.flaws" :key="'wpef' + j">
                <h1>{{ flaw_img }}</h1>
              </div>
            </draggable>
          </div>
        </draggable>

        <b-field position="is-right">
          <b-button type="is-dark" outlined :disabled="isLoading" @click="finish">Weiter</b-button>
        </b-field>
      </b-step-item>
    </b-steps>
  </div>
  </div>
</template>

<script>
import AutocompleteSelect from '../utility/AutocompleteSelect'
import draggable from 'vuedraggable'

import { mapGetters } from 'vuex'

export default {
  components: { AutocompleteSelect, draggable },
  name: "ViewWizard",
  data() {
    return {
      isLoading: false,
      activeStep: 0,
      protocolSkeleton: []
    }
  },
  computed: {
    ...mapGetters('wizard', ['facility', 'images', 'isPreprocessingWorking'])
  },
  methods: {
    prepare() {
      if (this.facility.id === null) {
        return;
      }

      this.isLoading = true;
      const cont = () => {
        console.log("TODO");
        fetch("/api/_autocompose", {
          method: "POST",
          body: {}
        });
      };

      const poll = setInterval(() => {
        if (!this.isPreprocessingWorking) {
          clearInterval(poll);
          cont();
        }
      }, 300);
    },
    finish() {

    }
  }
}
</script>

<style>

</style>
